from app.models.comentario import Comentario
from app.models.comentario_detalle import ComentarioDetalle
from app.db import get_connection


class ComentarioRepository:

    def create(self, contenido, usuario_id, sueno_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                            INSERT INTO comentario(contenido, usuario_id, sueno_id)
                            VALUES(%s, %s, %s)
                            RETURNING id, contenido, fecha_creacion, usuario_id, sueno_id
                            """,
                    (contenido, usuario_id, sueno_id),
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
                            RETURNING id, contenido, fecha_creacion, usuario_id, sueno_id
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
                            SELECT id, contenido, fecha_creacion, usuario_id, sueno_id
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
                            SELECT id, contenido, fecha_creacion, usuario_id, sueno_id
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
                            SELECT id, contenido, fecha_creacion, usuario_id, sueno_id
                            FROM comentario
                            WHERE usuario_id = %s
                            ORDER BY fecha_creacion DESC
                            """,
                    (usuario_id,),
                )
                rows = cur.fetchall()
                return [Comentario(*row) for row in rows]

    # Usaremos esta funcion para obtener los comentarios con el nombre de usuarios
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
                        u.avatar_url
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
                        u.avatar_url
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
