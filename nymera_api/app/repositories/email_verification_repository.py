from datetime import datetime

from app.db import get_connection
from app.models.email_verification_token import EmailVerificationToken


class EmailVerificationRepository:
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
                    INSERT INTO email_verification_token (
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

    def get_by_token(self, token: str):
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
                    FROM email_verification_token
                    WHERE token = %s
                    """,
                    (token,),
                )
                row = cur.fetchone()

                if row is None:
                    return None

                return EmailVerificationToken(*row)

    def mark_as_used(self, token_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE email_verification_token
                    SET usado = TRUE
                    WHERE id = %s
                    """,
                    (token_id,),
                )

                return cur.rowcount > 0

    def invalidate_user_tokens(self, usuario_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE email_verification_token
                    SET usado = TRUE
                    WHERE usuario_id = %s AND usado = FALSE
                    """,
                    (usuario_id,),
                )

    def get_latest_by_user(self, usuario_id):
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
                    FROM email_verification_token
                    WHERE usuario_id = %s
                    ORDER BY fecha_creacion DESC
                    LIMIT 1
                    """,
                    (usuario_id,),
                )
                row = cur.fetchone()

                if row is None:
                    return None

                return EmailVerificationToken(*row)

    def get_seconds_since_last_token(self, usuario_id) -> float | None:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT EXTRACT(EPOCH FROM (NOW() - fecha_creacion))
                    FROM email_verification_token
                    WHERE usuario_id = %s
                    ORDER BY fecha_creacion DESC
                    LIMIT 1
                    """,
                    (usuario_id,),
                )
                row = cur.fetchone()

                if row is None or row[0] is None:
                    return None

                return float(row[0])