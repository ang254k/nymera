from datetime import datetime, timedelta, timezone
from app.db import get_connection

class SecurityLogRepository:
    def create_log(
        self,
        evento: str,
        ip_address: str,
        email_intentado: str | None = None,
        user_agent: str | None = None,
        exito: bool = False
    ):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO security_logs (evento, email_intentado, ip_address, user_agent, exito, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            evento, 
                            email_intentado, 
                            ip_address, 
                            user_agent, 
                            exito, 
                            datetime.now(timezone.utc)
                        )
                    )
                    
                    #Limpieza de los 7 días
                    hace_siete_dias = datetime.now(timezone.utc) - timedelta(days=7)
                    cur.execute(
                        "DELETE FROM security_logs WHERE created_at < %s",
                        (hace_siete_dias,)
                    )
                conn.commit()
        except Exception as e:
            print(f"Error guardando security log: {e}")