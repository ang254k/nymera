from app.db import get_connection
from app.models.hashtag import Hashtag
from app.models.sueno_feed_detalle import SuenoFeedDetalle
from app.repositories.filtro_repository import FiltroRepository


class HashtagRepository(FiltroRepository):

    SUENO_FEED_SELECT = """
        SELECT
            s.id,
            s.titulo,
            LEFT(s.contenido, 200) AS preview_contenido,
            s.publico,
            s.fecha_creacion,
            s.usuario_id,

            COALESCE(
                u.nombre,
                'Usuario eliminado'
            ) AS usuario_nombre,

            u.avatar_url,

            cat.nombre AS categoria_nombre,

            COUNT(DISTINCT sl.usuario_id) AS likes_count,

            COUNT(DISTINCT c.id) AS comentarios_count,

            CASE
                WHEN MAX(sl_user.usuario_id) IS NOT NULL
                THEN TRUE
                ELSE FALSE
            END AS liked_by_user

        FROM sueno s

        LEFT JOIN usuario u
            ON u.id = s.usuario_id

        LEFT JOIN categoria cat
            ON cat.id = s.categoria_id

        LEFT JOIN sueno_like sl
            ON sl.sueno_id = s.id

        LEFT JOIN comentario c
            ON c.sueno_id = s.id

        LEFT JOIN sueno_like sl_user
            ON sl_user.sueno_id = s.id
            AND sl_user.usuario_id = %s
    """

    def get_by_nombre(self, nombre):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, nombre
                    FROM hashtag
                    WHERE LOWER(nombre) = LOWER(%s)
                    """,
                    (nombre,),
                )

                row = cur.fetchone()

                if row is None:
                    return None

                return Hashtag(*row)

    def insert(self, nombre):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO hashtag (nombre)
                    VALUES (%s)
                    RETURNING id, nombre
                    """,
                    (nombre,),
                )

                row = cur.fetchone()

                return Hashtag(*row)

    def insert_sueno_hashtag(self, sueno_id, hashtag_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO sueno_hashtag (
                        sueno_id,
                        hashtag_id
                    )
                    VALUES (%s, %s)
                    """,
                    (sueno_id, hashtag_id),
                )

    def delete_relaciones_sueno(self, sueno_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM sueno_hashtag
                    WHERE sueno_id = %s
                    """,
                    (sueno_id,),
                )

    def get_suenos_by_nombre(
        self, hashtag, usuario_id, categorias=None, ordenar_por=None, direccion=None
    ):
        where_extra, parametros, order_by = self.construir_filtros_y_orden(
            categorias,
            ordenar_por,
            direccion,
        )
        query = f"""
            {self.SUENO_FEED_SELECT}

            INNER JOIN sueno_hashtag sh
                ON s.id = sh.sueno_id

            INNER JOIN hashtag h
                ON h.id = sh.hashtag_id

            WHERE 
                LOWER(h.nombre) = LOWER(%s)
                AND s.publico = TRUE
                
            {where_extra}
            
            GROUP BY 
                s.id,
                u.nombre,
                u.avatar_url,
                cat.nombre

            {order_by}
            
        """

        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute(
                    query,
                    (
                        usuario_id,
                        hashtag,
                        *parametros
                    ),
                )

                rows = cur.fetchall()
                return [SuenoFeedDetalle(*row) for row in rows]

    def get_trending(self, limit=10):
        query = """
            SELECT
                h.nombre,
                COUNT(*) num_usos
            FROM hashtag h

            INNER JOIN sueno_hashtag sh
                ON sh.hashtag_id = h.id

            INNER JOIN sueno s
                ON s.id = sh.sueno_id

            WHERE 
                s.publico = TRUE

            GROUP BY
                h.id,
                h.nombre

            ORDER BY COUNT(*) DESC

            LIMIT %s
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (limit,))
                rows = cur.fetchall()

                return [row[0] for row in rows]
