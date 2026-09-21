import resend

from app.config import settings


class EmailService:

    def __init__(self):
        resend.api_key = settings.RESEND_API_KEY

    def enviar_email_prueba(self, destino: str):

        params = {
            "from": "onboarding@resend.dev",
            "to": destino,
            "subject": "Prueba Nymera",
            "html": "<h1> ¡Hola desde Nymera!🌙</h1>",
        }

        return resend.Emails.send(params)

    def enviar_email_recuperacion(
        self,
        destinatario,
        reset_url,
    ):
        params = {
            "from": "onboarding@resend.dev",
            "to": destinatario,
            "subject": "Recuperacioón de contraseña",
            "html": f"""
            <h2>Recuperación de contraseña</h2>

            <p>Hola.</p>

            <p>Has solicitado recuperar tu contraseña.</p>

            <p>
                Pulsa en el siguiente enlace:
            </p>

            <p>
                <a href="{reset_url}">
                    Restablecer contraseña
                </a>
            </p>

            <p>
                Este enlace expirará en 30 minutos.
            </p>

            <p>
                Si no has solicitado este cambio,
                puedes ignorar este correo.
            </p>
                    """,
        }
        
        return resend.Emails.send(params)
