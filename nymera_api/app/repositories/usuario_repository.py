from app.db import get_connection
from app.models.usuario import Usuario
from psycopg import errors


class UsuarioRepository:

    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT id, nombre, email, NULL, fecha_creacion, avatar_url
                        FROM usuario"""
                )
                rows = cur.fetchall()

                return [Usuario(id=row[0], nombre=row[1], email=row[2]) for row in rows]

    def get_by_email(self, email):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, email, password, fecha_creacion, avatar_url
                    FROM usuario
                    WHERE email = %s
                    """,
                    (email,),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                return Usuario(*row)

    def get_by_id(self, id: int) -> Usuario | None:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, email, NULL, fecha_creacion, avatar_url
                    FROM usuario
                    WHERE id = %s
                    """,
                    (id,),
                )
                row = cur.fetchone()
                if row is None:
                    return None

                return Usuario(*row)

    def update_perfil(self, user_id, nombre=None):
        with get_connection() as conn:
            with conn.cursor() as cur:

                campos = []
                valores = []

                if nombre:
                    campos.append("nombre = %s")
                    valores.append(nombre)

                if not campos:
                    return False

                valores.append(user_id)

                query = f"""
                    UPDATE usuario
                    SET {", ".join(campos)}
                    WHERE id = %s
                """
                cur.execute(query, tuple(valores))

                return cur.rowcount > 0

    def update_password(self, user_id, password_hash):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE usuario
                SET password = %s
                WHERE id = %s
                """,
                (password_hash, user_id)
                )
                
                return cur.rowcount > 0

    def get_by_nombre(self, user):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, email, password, fecha_creacion, avatar_url
                    FROM usuario
                    WHERE nombre = %s
                    """,
                    (user,),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                return Usuario(*row)

    def insert(self, nombre, email: str, password: str):
        with get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO usuario (nombre, email, password) VALUES (%s, %s, %s)
                        RETURNING id, nombre, email, NULL, fecha_creacion, avatar_url
                        """,
                        (nombre, email, password),
                    )
                    row = cur.fetchone()
                    return Usuario(*row)

            except errors.UniqueViolation:
                conn.rollback()
                return None

            except Exception:
                conn.rollback()
                raise

    def delete(self, user_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM usuario WHERE id = %s", (user_id,))
                return cur.rowcount > 0

    def get_by_id_with_password(self, id: int) -> Usuario | None:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, email, password
                    FROM usuario
                    WHERE id = %s
                    """,
                    (id,),
                )

                row = cur.fetchone()

                if row is None:
                    return None

                return Usuario(*row)

    def update_avatar(self, usuario_id, avatar_url):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE usuario
                    SET avatar_url = %s
                    WHERE id = %s
                    RETURNING id, nombre, email, NULL, fecha_creacion, avatar_url
                    """,
                    (avatar_url, usuario_id),
                )

                row = cur.fetchone()

                if row is None:
                    return None

                return Usuario(*row)
