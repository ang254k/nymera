from app.db import get_connection
from app.models.sueno import Sueno
from app.models.sueno_feed_detalle import SuenoFeedDetalle
from app.models.sueno_detalle import SuenoDetalle


class SuenoRepository:

    def create(self, titulo, contenido, usuario_id, categoria_id, publico=True):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO sueno (titulo, contenido, usuario_id, categoria_id, publico)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, titulo, contenido, publico, fecha_creacion, usuario_id, categoria_id
                    """,
                    (titulo, contenido, usuario_id, categoria_id, publico),
                )
                row = cur.fetchone()
                return Sueno(*row)

    def update(self, sueno_id, titulo, contenido, categoria_id, publico):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE sueno
                    SET titulo = %s,
                        contenido = %s,
                        categoria_id = %s,
                        publico = %s
                    WHERE id = %s
                    RETURNING id, titulo, contenido, publico, fecha_creacion, usuario_id, categoria_id
                """,
                    (titulo, contenido, categoria_id, publico, sueno_id),
                )

                row = cur.fetchone()
                if not row:
                    return None

                return Sueno(*row)

    def delete(self, sueno_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM sueno
                    WHERE id = %s
                    RETURNING id
                """,
                    (sueno_id,),
                )
                row = cur.fetchone()
                return row is not None

    def get_by_id(self, sueno_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, titulo, contenido, publico, fecha_creacion, usuario_id, categoria_id
                    FROM sueno
                    WHERE id = %s
                    """,
                    (sueno_id,),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                return Sueno(*row)

    # Detalles de los suenos
    def get_detalles(
        self,
        usuario_id,
        sueno_id,
    ):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        s.id,
                        s.titulo,
                        s.contenido,
                        s.publico,
                        s.fecha_creacion,
                        s.usuario_id,
                        s.categoria_id,
                        u.nombre AS usuario_nombre,
                        u.avatar_url AS avatar_url,
                        cat.nombre AS categoria_nombre,

                        COUNT(DISTINCT sl.usuario_id) AS likes_count,
                        COUNT(DISTINCT c.id) AS comentarios_count,

                        CASE 
                            WHEN MAX(sl_user.usuario_id) IS NOT NULL THEN TRUE
                            ELSE FALSE
                        END AS liked_by_user

                    FROM sueno s

                    LEFT JOIN usuario u ON u.id = s.usuario_id

                    LEFT JOIN sueno_like sl ON sl.sueno_id = s.id

                    LEFT JOIN comentario c ON c.sueno_id = s.id
                    
                    LEFT JOIN categoria cat ON cat.id = s.categoria_id
                    
                    LEFT JOIN sueno_like sl_user
                        ON sl_user.sueno_id = s.id
                        AND sl_user.usuario_id = %s

                    WHERE s.id = %s

                    GROUP BY s.id, u.nombre, u.avatar_url, cat.nombre
                    """,
                    (
                        usuario_id,
                        sueno_id,
                    ),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                return SuenoDetalle(*row)

    def get_all_by_user(self, usuario_id):
        # Muestra todos los sueños(Para ver el perfil de uno mismo)
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                           SELECT id, titulo, contenido, publico, fecha_creacion, usuario_id, categoria_id
                           FROM sueno
                           WHERE usuario_id = %s
                           ORDER BY fecha_creacion DESC
                           """,
                    (usuario_id,),
                )
                rows = cur.fetchall()
                return [Sueno(*row) for row in rows]

    # Suenos publicos
    def get_public_by_user(self, usuario_id):
        # Muestra solo los sueños publicos(Cuando un usuario visita el perfil ajeno)
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                           SELECT id, titulo, contenido, publico, fecha_creacion, usuario_id, categoria_id
                           FROM sueno
                           WHERE usuario_id = %s
                           and publico = TRUE
                           ORDER BY fecha_creacion DESC
                           """,
                    (usuario_id,),
                )

                rows = cur.fetchall()
                return [Sueno(*row) for row in rows]

    def count_public(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*)
                    FROM sueno
                    WHERE publico = TRUE
                """)
                return cur.fetchone()[0]

    def get_feed_detalle(
        self,
        usuario_id: int | None,
        limit: int,
        offset: int,
        categorias: list[int] | None = None,
        ordenar_por: str | None = None,
        direccion: str | None = None,
    ):

        where_extra, parametros, order_by = self.construir_filtros_y_orden(
            categorias, ordenar_por, direccion
        )

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                            SELECT
                                s.id,
                                s.titulo,
                                s.contenido,
                                s.publico,
                                s.fecha_creacion,
                                s.usuario_id,
                                COALESCE(u.nombre, 'Usuario eliminado') AS usuario_nombre,
                                u.avatar_url,
                                cat.nombre AS categoria_nombre,
                                COUNT(DISTINCT sl.usuario_id) AS likes_count,
                                COUNT(DISTINCT c.id) AS comentarios_count,

                                CASE 
                                    WHEN MAX(sl_user.usuario_id) IS NOT NULL THEN TRUE
                                    ELSE FALSE
                                END AS liked_by_user

                            FROM sueno s

                            LEFT JOIN usuario u ON u.id = s.usuario_id

                            LEFT JOIN categoria cat ON cat.id = s.categoria_id

                            LEFT JOIN sueno_like sl 
                                ON sl.sueno_id = s.id

                            
                            LEFT JOIN comentario c 
                                ON c.sueno_id = s.id

                            LEFT JOIN sueno_like sl_user
                            ON sl_user.sueno_id = s.id
                            AND sl_user.usuario_id = %s

                            WHERE s.publico = TRUE
                            
                            {where_extra}
                            
                            GROUP BY s.id, u.nombre, u.avatar_url, cat.nombre

                            {order_by}

                            LIMIT %s OFFSET %s

                            """,
                    (usuario_id, *parametros, limit, offset),
                )

                rows = cur.fetchall()
                feed_items = []

                for row in rows:
                    row = list(row)
                    row[2] = self._crear_preview(row[2])
                    feed_items.append(SuenoFeedDetalle(*row))

                return feed_items

    def get_feed_by_user(
        self,
        perfil_usuario_id,
        usuario_actual_id=None,
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
                    SELECT
                        s.id,
                        s.titulo,
                        LEFT(s.contenido, 120) AS preview_contenido,
                        s.publico,
                        s.fecha_creacion,
                        s.usuario_id,
                        u.nombre AS usuario_nombre,
                        u.avatar_url,
                        cat.nombre AS categoria_nombre,

                        COUNT(DISTINCT sl.usuario_id) AS likes_count,
                        COUNT(DISTINCT c.id) AS comentarios_count,

                        CASE
                            WHEN MAX(sl_user.usuario_id) IS NOT NULL THEN TRUE
                            ELSE FALSE
                        END AS liked_by_user

                    FROM sueno s

                    LEFT JOIN usuario u ON u.id = s.usuario_id
                    LEFT JOIN sueno_like sl ON sl.sueno_id = s.id
                    LEFT JOIN comentario c ON c.sueno_id = s.id
                    
                    LEFT JOIN categoria cat ON cat.id = s.categoria_id

                    LEFT JOIN sueno_like sl_user
                        ON sl_user.sueno_id = s.id
                        AND sl_user.usuario_id = %s

                    WHERE s.usuario_id = %s
                    AND (s.publico = TRUE OR s.usuario_id = %s)
                    
                    {where_extra}

                    GROUP BY s.id, u.nombre, u.avatar_url, cat.nombre
                    {order_by}
                """,
                    (
                        usuario_actual_id,
                        perfil_usuario_id,
                        usuario_actual_id,
                        *parametros,
                    ),
                )

                rows = cur.fetchall()

                return [SuenoFeedDetalle(*row) for row in rows]

    # Sueños likeados por usuario X
    def get_liked_by_user(
        self,
        perfil_usuario_id,
        usuario_actual_id=None,
        categorias=None,
        ordenar_por=None,
        direccion=None,
    ):
        where_extra, parametros, order_by = self.construir_filtros_y_orden(
            categorias, ordenar_por, direccion, "ORDER BY liked.fecha DESC"
        )
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
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

                    FROM sueno_like liked

                    JOIN sueno s
                        ON s.id = liked.sueno_id

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

                    WHERE liked.usuario_id = %s
                    AND (
                        s.publico = TRUE
                        OR s.usuario_id = %s
                    )
                    
                    {where_extra}
                    
                    GROUP BY
                        s.id,
                        u.nombre,
                        u.avatar_url,
                        cat.nombre,
                        liked.fecha

                    {order_by}
                    """,
                    (
                        usuario_actual_id,
                        perfil_usuario_id,
                        perfil_usuario_id,
                        *parametros,
                    ),
                )

                rows = cur.fetchall()

                return [SuenoFeedDetalle(*row) for row in rows]

    def get_feed_item_by_id(self, sueno_id, usuario_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        s.id,
                        s.titulo,
                        LEFT(s.contenido, 200) AS preview_contenido,
                        s.publico,
                        s.fecha_creacion,
                        s.usuario_id,
                        COALESCE(u.nombre, 'Usuario eliminado') AS usuario_nombre,
                        u.avatar_url,
                        cat.nombre AS categoria_nombre,
                        COUNT(DISTINCT sl.usuario_id) AS likes_count,
                        COUNT(DISTINCT c.id) AS comentarios_count,

                        CASE
                            WHEN MAX(sl_user.usuario_id) IS NOT NULL THEN TRUE
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

                    WHERE s.id = %s

                    GROUP BY s.id, u.nombre, u.avatar_url, cat.nombre
                    """,
                    (usuario_id, sueno_id),
                )

                row = cur.fetchone()

                if row is None:
                    return None

                return SuenoFeedDetalle(*row)

    def construir_filtros_y_orden(
        self,
        categorias=None,
        ordenar_por=None,
        direccion=None,
        orden_defecto="ORDER BY s.fecha_creacion DESC",
    ):
        where_extra = ""
        parametros = []

        if categorias:
            where_extra += """
            AND s.categoria_id = ANY(%s)
            """
            parametros.append(categorias)

        campos = {
            "fecha": "s.fecha_creacion",
            "likes": "likes_count",
            "comentarios": "comentarios_count",
        }

        order_by = orden_defecto

        if ordenar_por in campos:
            campo = campos[ordenar_por]

            if direccion == "asc":
                order_by = f"ORDER BY {campo} ASC"
            elif direccion == "desc":
                order_by = f"ORDER BY {campo} DESC"

        return where_extra, parametros, order_by

    def _crear_preview(self, contenido: str, limite: int = 200) -> str:
        if len(contenido) <= limite:
            return contenido

        preview = contenido[:limite]

        # Elimina la ultima palabra
        preview = preview.rsplit(" ", 1)[0]

        return preview.rstrip() + "..."
