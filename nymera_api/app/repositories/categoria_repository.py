from app.db import get_connection
from app.models.categoria import Categoria

class CategoriaRepository:
    def get_by_id(self,id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id, nombre
                            FROM categoria
                            WHERE id = %s
                            """,
                            (id,)
                            )
                row = cur.fetchone()
                if row is None:
                    return None
                return Categoria(*row)
            
    def get_by_nombre(self,nombre):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id, nombre
                            FROM categoria
                            WHERE nombre = %s
                            """,
                            (nombre,)
                            )
                row = cur.fetchone()
                if row is None:
                    return None
                return Categoria(*row)
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id, nombre
                            FROM categoria
                            ORDER BY nombre ASC
                            """
                            )
                rows = cur.fetchall()
                return [Categoria(*row) for row in rows]
