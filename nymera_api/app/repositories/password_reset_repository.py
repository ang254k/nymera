from datetime import datetime

from app.db import get_connection
from app.models.password_reset_token import PasswordResetToken


class PasswordResetRepository:
    def create_token(
        self,
        usuario_id,
        token: str,
        fecha_expiracion: datetime,
    ):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO password_reset_token (
                        usuario_id,
                        token,
                        fecha_expiracion
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        usuario_id,
                        token,
                        fecha_expiracion,
                    ),
                )

    def get_by_token(self, token):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        usuario_id,
                        token,
                        fecha_creacion,
                        fecha_expiracion,
                        usado
                    FROM password_reset_token
                    WHERE token = %s
                    """,
                    (token,),
                )
                row = cur.fetchone()
                
                if row is None:
                    return None
                
                return PasswordResetToken(*row)

    def mark_as_used(self, token_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE password_reset_token
                    SET usado = TRUE
                    WHERE id = %s
                    """,
                    (token_id,),
                )
                
                return cur.rowcount > 0
