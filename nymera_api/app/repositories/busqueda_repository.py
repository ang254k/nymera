from app.db import get_connection
from app.models.sueno_feed_detalle import SuenoFeedDetalle
from app.repositories.filtro_repository import FiltroRepository

class BusquedaRepository(FiltroRepository):

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

    def search_usuarios(self, termino):

        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        avatar_url
                    FROM usuario
                    WHERE unaccent(nombre) ILIKE unaccent(%s)
                    LIMIT 10
                    """,
                    (f"%{termino}%",),
                )

                return cur.fetchall()

    def search_suenos(
        self,
        termino,
        usuario_id,
        categorias=None,
        ordenar_por=None,
        direccion=None,
    ):

        where_extra, parametros, order_by = self.construir_filtros_y_orden(
            categorias, ordenar_por, direccion
        )

        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute(
                    f"""
                    {self.SUENO_FEED_SELECT}

                    WHERE s.publico = TRUE
                    AND (
                        unaccent(s.titulo) ILIKE unaccent(%s)
                        OR unaccent(s.contenido) ILIKE unaccent(%s)
                    )
                    
                    {where_extra}
                    
                    GROUP BY
                        s.id,
                        u.nombre,
                        u.avatar_url,
                        cat.nombre

                    {order_by}

                    LIMIT 20
                    """,
                    (usuario_id, f"%{termino}%", f"%{termino}%", *parametros),
                )

                rows = cur.fetchall()

                return [SuenoFeedDetalle(*row) for row in rows]

    def get_suenos_multiple_words(
        self,
        palabras,
        usuario_id,
        categorias=None,
        ordenar_por=None,
        direccion=None,
    ):
        where_extra, parametros, order_by = self.construir_filtros_y_orden(
            categorias, ordenar_por, direccion
        )

        conditions = []
        params = [usuario_id]

        for palabra in palabras:
            conditions.append(
                "(unaccent(s.titulo) ILIKE unaccent(%s) OR unaccent(s.contenido) ILIKE unaccent(%s))"
            )

            params.append(f"%{palabra}%")
            params.append(f"%{palabra}%")
        
        params.extend(parametros)
            
        query = f"""
                {self.SUENO_FEED_SELECT}
                
                WHERE 
                    s.publico = TRUE
                AND(
                    {' AND '.join(conditions)}
                )
                
                {where_extra}
                
                GROUP BY
                    s.id,
                    u.nombre,
                    u.avatar_url,
                    cat.nombre
                
                {order_by}
                
                LIMIT 20
            """

        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute(query, tuple(params))

                rows = cur.fetchall()

                return [SuenoFeedDetalle(*row) for row in rows]

    def get_suenos_by_hashtag(
        self,
        hashtags,
        usuario_id,
        categorias=None,
        ordenar_por=None,
        direccion=None,
    ):
        where_extra, parametros, order_by = self.construir_filtros_y_orden(
            categorias, ordenar_por, direccion
        )
        placeholders = ",".join(["%s"] * len(hashtags))

        query = f"""
            {self.SUENO_FEED_SELECT}

            INNER JOIN sueno_hashtag sh
                ON s.id = sh.sueno_id

            INNER JOIN hashtag h
                ON h.id = sh.hashtag_id

            WHERE 
                LOWER(h.nombre) IN ({placeholders})
                AND s.publico = TRUE
                
            {where_extra}
            
            GROUP BY 
                s.id,
                u.nombre,
                u.avatar_url,
                cat.nombre

            HAVING COUNT(DISTINCT h.nombre) = %s

            {order_by}
        """

        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute(query, (usuario_id, *hashtags, len(hashtags), *parametros))

                rows = cur.fetchall()
                return [SuenoFeedDetalle(*row) for row in rows]
