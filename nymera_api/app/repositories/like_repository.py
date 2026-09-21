from app.db import get_connection
from app.models.like import Like

class LikeRepository:

    def add_like(self, usuario_id, sueno_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO sueno_like(usuario_id, sueno_id)
                            VALUES(%s, %s)
                            RETURNING usuario_id, sueno_id, fecha
                            """,
                            (usuario_id, sueno_id)
                            )
                row = cur.fetchone()
                return Like(*row)
    def remove_like(self, usuario_id, sueno_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            DELETE FROM sueno_like
                            WHERE usuario_id = %s AND sueno_id = %s
                            """,
                            (usuario_id, sueno_id)
                            )
                # if cur.rowcount == 0:
                #     return False
                # return True
                return cur.rowcount > 0
            
    def count_by_sueno(self, sueno_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT COUNT(*)
                            FROM sueno_like
                            WHERE sueno_id = %s
                            """, 
                            (sueno_id,)
                            )

                row = cur.fetchone()
                return row[0]

    def exists(self, usuario_id, sueno_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 1
                    FROM sueno_like
                    WHERE usuario_id = %s AND sueno_id = %s
                """, (usuario_id, sueno_id))

                return cur.fetchone() is not None