import httpx
from app.config import settings


class EmailService:
    BREVO_URL = "https://api.brevo.com/v3/smtp/email"

    def __init__(self):
        self.api_key = settings.BREVO_API_KEY
        self.sender = {
            "name": settings.EMAIL_FROM_NAME,
            "email": settings.EMAIL_FROM,
        }
        self.logo_url = getattr(settings, "EMAIL_LOGO_URL", None)

    def _enviar_email(self, destinatario: str, subject: str, html_content: str):
        headers = {
            "accept": "application/json",
            "api-key": self.api_key,
            "content-type": "application/json",
        }
        payload = {
            "sender": self.sender,
            "to": [{"email": destinatario}],
            "subject": subject,
            "htmlContent": html_content,
        }

        with httpx.Client(timeout=10.0) as client:
            response = client.post(self.BREVO_URL, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()

    def _construir_plantilla_html(
        self,
        titulo: str,
        saludo: str,
        cuerpo: str,
        texto_boton: str,
        url_boton: str,
        nota_expiracion: str,
        nota_seguridad: str,
        texto_enlace_alternativo: str,
    ) -> str:
        logo_html = (
            f'<img src="{self.logo_url}" alt="Nymera" width="155" '
            f'style="display:block; width:155px; max-width:100%; height:auto; margin:0 auto; border:0;" />'
            if self.logo_url
            else '<span style="font-size:22px; font-weight:700; letter-spacing:1.5px; color:#c77dff;">NYMERA</span>'
        )

        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        </head>
        <body style="margin:0; padding:0; background-color:#0b0a12; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color:#e6e4f0;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color:#0b0a12; padding:32px 16px;">
                <tr>
                    <td align="center">
                        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width:520px; background-color:#12101c; border:1px solid #26223a; border-radius:16px; overflow:hidden;">
                            
                            <!-- Cabecera / Banner de marca -->
                            <tr>
                                <td align="center" style="padding:28px 24px 22px 24px; background:linear-gradient(180deg, #1b172b 0%, #12101c 100%); border-bottom:1px solid #221e34;">
                                    {logo_html}
                                    <div style="width:155px; height:2px; background-color:#64e0d0; margin:14px auto 0 auto; border-radius:2px;"></div>
                                </td>
                            </tr>

                            <!-- Contenido principal -->
                            <tr>
                                <td style="padding:32px 28px 24px 28px;">
                                    <h1 style="margin:0 0 16px 0; font-size:20px; font-weight:600; color:#ffffff;">
                                        {titulo}
                                    </h1>
                                    <p style="margin:0 0 12px 0; font-size:15px; line-height:1.6; color:#cfcce0;">
                                        {saludo}
                                    </p>
                                    <p style="margin:0 0 26px 0; font-size:15px; line-height:1.6; color:#cfcce0;">
                                        {cuerpo}
                                    </p>

                                    <!-- Botón CTA -->
                                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                        <tr>
                                            <td align="center" style="padding:4px 0 26px 0;">
                                                <a href="{url_boton}" target="_blank" style="display:inline-block; padding:13px 28px; background-color:#c77dff; color:#12101c; font-size:15px; font-weight:700; text-decoration:none; border-radius:10px;">
                                                    {texto_boton}
                                                </a>
                                            </td>
                                        </tr>
                                    </table>

                                    <p style="margin:0 0 10px 0; font-size:13px; line-height:1.5; color:#64e0d0;">
                                        {nota_expiracion}
                                    </p>
                                    <p style="margin:0; font-size:13px; line-height:1.5; color:#9691b0;">
                                        {nota_seguridad}
                                    </p>
                                </td>
                            </tr>

                            <!-- Enlace alternativo + Footer -->
                            <tr>
                                <td style="padding:18px 28px 26px 28px; background-color:#0f0d18; border-top:1px solid #221e34;">
                                    <p style="margin:0 0 8px 0; font-size:12px; line-height:1.5; color:#7c7796;">
                                        {texto_enlace_alternativo}
                                    </p>
                                    <p style="margin:0; font-size:11px; line-height:1.4; word-break:break-all; color:#9d97ba;">
                                        <a href="{url_boton}" style="color:#64e0d0; text-decoration:underline;">{url_boton}</a>
                                    </p>
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

    def enviar_email_prueba(self, destino: str):
        return self._enviar_email(
            destinatario=destino,
            subject="Prueba Nymera",
            html_content="<h1>¡Hola desde Nymera! 🌙</h1>",
        )

    def enviar_email_recuperacion(
        self,
        destinatario: str,
        reset_url: str,
        lang: str = "es",
    ):
        is_en = (lang or "es").lower().startswith("en")

        if is_en:
            subject = "Reset your Nymera password"
            html_content = self._construir_plantilla_html(
                titulo="Password reset",
                saludo="Hello,",
                cuerpo="We received a request to reset the password for your Nymera account. Click the button below to choose a new one:",
                texto_boton="Reset password",
                url_boton=reset_url,
                nota_expiracion="This link will expire in 30 minutes.",
                nota_seguridad="If you did not request this change, you can safely ignore this email.",
                texto_enlace_alternativo="If the button doesn't work, copy and paste this link into your browser:",
            )
        else:
            subject = "Recuperación de contraseña en Nymera"
            html_content = self._construir_plantilla_html(
                titulo="Recuperación de contraseña",
                saludo="Hola,",
                cuerpo="Hemos recibido una solicitud para restablecer la contraseña de tu cuenta en Nymera. Pulsa el siguiente botón para elegir una nueva:",
                texto_boton="Restablecer contraseña",
                url_boton=reset_url,
                nota_expiracion="Este enlace expirará en 30 minutos.",
                nota_seguridad="Si no has solicitado este cambio, puedes ignorar este correo de forma segura.",
                texto_enlace_alternativo="Si el botón no funciona, copia y pega este enlace en tu navegador:",
            )

        return self._enviar_email(
            destinatario=destinatario,
            subject=subject,
            html_content=html_content,
        )

    def enviar_email_verificacion(
        self,
        destinatario: str,
        verify_url: str,
        lang: str = "es",
    ):
        is_en = (lang or "es").lower().startswith("en")

        if is_en:
            subject = "Verify your Nymera account"
            html_content = self._construir_plantilla_html(
                titulo="Verify your email address",
                saludo="Hello,",
                cuerpo="Thanks for joining Nymera. Click the button below to verify your email address and activate your account:",
                texto_boton="Verify account",
                url_boton=verify_url,
                nota_expiracion="This verification link will expire in 24 hours.",
                nota_seguridad="If you did not create a Nymera account, you can safely ignore this email.",
                texto_enlace_alternativo="If the button doesn't work, copy and paste this link into your browser:",
            )
        else:
            subject = "Verifica tu cuenta en Nymera"
            html_content = self._construir_plantilla_html(
                titulo="Verifica tu correo electrónico",
                saludo="Hola,",
                cuerpo="Gracias por unirte a Nymera. Pulsa el siguiente botón para verificar tu correo electrónico y activar tu cuenta:",
                texto_boton="Verificar cuenta",
                url_boton=verify_url,
                nota_expiracion="Este enlace de verificación expirará en 24 horas.",
                nota_seguridad="Si no has creado una cuenta en Nymera, puedes ignorar este correo de forma segura.",
                texto_enlace_alternativo="Si el botón no funciona, copia y pega este enlace en tu navegador:",
            )

        return self._enviar_email(
            destinatario=destinatario,
            subject=subject,
            html_content=html_content,
        )
