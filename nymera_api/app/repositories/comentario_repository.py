from app.models.comentario import Comentario
from app.models.comentario_detalle import ComentarioDetalle
from app.db import get_connection


class ComentarioRepository:

    def create(self, contenido, usuario_id, sueno_id, idioma_original="es"):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                            INSERT INTO comentario(
                                contenido, usuario_id, sueno_id, idioma_original
                            )
                            VALUES(%s, %s, %s, %s)
                            RETURNING id, contenido, fecha_creacion, usuario_id, sueno_id, idioma_original
                            """,
                    (contenido, usuario_id, sueno_id, idioma_original),
                )
                row = cur.fetchone()
                return Comentario(*row)

    def update(self, contenido_nuevo, comentario_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE comentario SET contenido= %s
                    WHERE id = %s
                    RETURNING id, contenido, fecha_creacion, usuario_id, sueno_id, idioma_original
                    """,
                    (contenido_nuevo, comentario_id),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                return Comentario(*row)

    def delete(self, comentario_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                            DELETE FROM comentario
                            WHERE id = %s
                            """,
                    (comentario_id,),
                )
                return cur.rowcount > 0

    def get_by_id(self, comentario_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, contenido, fecha_creacion, usuario_id, 
                            sueno_id, idioma_original
                    FROM comentario
                    WHERE id = %s
                    """,
                    (comentario_id,),
                )

                row = cur.fetchone()
                if row is None:
                    return None

                return Comentario(*row)

    # No queda obsoleta, por get_all_by_sueno, sino que sirve para validaciones
    def get_all_by_sueno(self, sueno_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, contenido, fecha_creacion, usuario_id, sueno_id, idioma_original
                    FROM comentario
                    WHERE sueno_id = %s
                    ORDER BY fecha_creacion DESC
                    """,
                    (sueno_id,),
                )
                rows = cur.fetchall()
                return [Comentario(*row) for row in rows]

    def get_all_by_usuario(self, usuario_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, contenido, fecha_creacion, usuario_id, sueno_id, idioma_original
                    FROM comentario
                    WHERE usuario_id = %s
                    ORDER BY fecha_creacion DESC
                    """,
                    (usuario_id,),
                )
                rows = cur.fetchall()
                return [Comentario(*row) for row in rows]

    # Obtener los comentarios con el nombre de usuarios
    def get_detalle_by_sueno(self, sueno_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.id,
                        c.contenido,
                        c.fecha_creacion,
                        c.usuario_id,
                        u.nombre,
                        u.avatar_url,
                        c.idioma_original
                    FROM comentario c
                    JOIN usuario u ON u.id = c.usuario_id
                    WHERE c.sueno_id = %s
                    ORDER BY c.fecha_creacion DESC
                    """,
                    (sueno_id,),
                )

                rows = cur.fetchall()
                return [ComentarioDetalle(*row) for row in rows]

    def get_detalle_by_id(self, comentario_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.id,
                        c.contenido,
                        c.fecha_creacion,
                        c.usuario_id,
                        u.nombre,
                        u.avatar_url,
                        c.idioma_original
                    FROM comentario c
                    JOIN usuario u ON u.id = c.usuario_id
                    WHERE c.id = %s
                    ORDER BY c.fecha_creacion DESC
                """,
                    (comentario_id,),
                )

                row = cur.fetchone()

                if row is None:
                    return None

                return ComentarioDetalle(*row)

    def get_traduccion(self, comentario_id, idioma):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT contenido
                    FROM comentario_traduccion
                    WHERE comentario_id = %s AND idioma = %s
                    """,
                    (comentario_id, idioma),
                )
                row = cur.fetchone()
                if row is None:
                    return None

                return row[0]

    def save_traduccion(self, comentario_id, idioma, contenido):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO comentario_traduccion (
                        comentario_id, idioma, contenido
                    )
                    VALUES (%s, %s, %s)
                    RETURNING contenido
                    """,
                    (comentario_id, idioma, contenido),
                )
                row = cur.fetchone()
                return row[0]

    def delete_traducciones(self, comentario_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM comentario_traduccion
                    WHERE comentario_id = %s
                    """,
                    (comentario_id,),
                )
