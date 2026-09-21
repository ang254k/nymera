from app.db import get_connection
from app.models.notificacion_detalle import NotificacionDetalle

class NotificacionRepository:

    def create(self, usuario_id, tipo, emisor_id, sueno_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO notificacion (usuario_id, tipo, emisor_id, sueno_id)
                    VALUES (%s, %s, %s, %s)
                """, (usuario_id, tipo, emisor_id, sueno_id))
                conn.commit()

    def get_by_user(self, usuario_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        n.id,
                        n.tipo,
                        u.nombre AS emisor_nombre,
                        n.sueno_id,
                        n.leido,
                        n.fecha_creacion
                    FROM notificacion n
                    LEFT JOIN usuario u ON u.id = n.emisor_id
                    WHERE n.usuario_id = %s
                    ORDER BY n.fecha_creacion DESC
                """, (usuario_id,))

                rows = cur.fetchall()

                return [NotificacionDetalle(*row) for row in rows]
            
    def marcar_como_leida(self, notificacion_id, usuario_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE notificacion
                    SET leido = TRUE
                    WHERE id = %s AND usuario_id = %s
                """, (notificacion_id, usuario_id))
                conn.commit()