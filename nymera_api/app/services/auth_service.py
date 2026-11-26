from passlib.hash import bcrypt
from app.config import settings

from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.password_reset_repository import PasswordResetRepository
from app.repositories.security_log_repository import SecurityLogRepository
from app.services.email_service import EmailService
from app.repositories.email_verification_repository import EmailVerificationRepository

from datetime import datetime, timedelta
import secrets


class AuthService:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
        self.reset_repo = PasswordResetRepository()
        self.verification_repo = EmailVerificationRepository()
        self.email_service = EmailService()
        self.security_log_repo = SecurityLogRepository()

    def forgot_password(self, email: str, lang: str = "es"):
        # Validacion
        usuario = self.usuario_repo.get_by_email(email)

        if usuario is None:
            return {
                "message": "password_reset_email_sent"
            }
        # Genera token
        token = secrets.token_urlsafe(32)
        # Expira en 30 min
        fecha_expiracion = datetime.now() + timedelta(minutes=30)

        self.reset_repo.create_token(usuario.id, token, fecha_expiracion)

        reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"

        self.email_service.enviar_email_recuperacion(
            usuario.email,
            reset_url,
            lang=lang
        )

        return {
            "message": "password_reset_email_sent"
        }

    def reset_password(self, token: str, new_password: str, ip_address: str = "unknown", user_agent: str = "unknown"):
        token_obj = self.reset_repo.get_by_token(token)
        #Validaciones
        #Existe?
        if token_obj is None:
            self.security_log_repo.create_log(
                evento="PASSWORD_RESET_INVALID",
                ip_address=ip_address,
                user_agent=user_agent,
                exito=False
            )
            raise ValueError("token_invalid")
        #Usado?
        if token_obj.usado:
            self.security_log_repo.create_log(
                evento="PASSWORD_RESET_USED",
                ip_address=ip_address,
                user_agent=user_agent,
                exito=False
            )
            raise ValueError("reset_link_used")
        #Fecha ok?
        if datetime.now() > token_obj.fecha_expiracion:
            self.security_log_repo.create_log(
                evento="PASSWORD_RESET_EXPIRED",
                ip_address=ip_address,
                user_agent=user_agent,
                exito=False
            )
            raise ValueError("reset_link_expired")

        #Se busca usuario
        usuario = self.usuario_repo.get_by_id_with_password(token_obj.usuario_id)

        if usuario is None:
            raise ValueError("user_not_found")
        
        if not new_password:
            raise ValueError("new_password_required")

        if len(new_password) < 8:
            raise ValueError("new_password_too_short")

        #Hash pw
        nuevo_hash = bcrypt.hash(new_password)
        
        #Actualiza usuario(pw)
        actualizado = self.usuario_repo.update_password(
            usuario.id,
            nuevo_hash
        )
        
        if not actualizado:
            raise ValueError("password_update_failed")
        #Se marca token
        marcado = self.reset_repo.mark_as_used(token_obj.id)
        
        if not marcado:
            raise ValueError("token_invalidation_failed")
        
        return{
            "message": "password_updated"
        }
        
    def verify_email(
        self,
        token: str,
        ip_address: str = "unknown",
        user_agent: str = "unknown",
    ):
        token_obj = self.verification_repo.get_by_token(token)

        if token_obj is None:
            self.security_log_repo.create_log(
                evento="EMAIL_VERIFY_INVALID",
                ip_address=ip_address,
                user_agent=user_agent,
                exito=False,
            )
            raise ValueError("token_invalid")

        if token_obj.usado:
            self.security_log_repo.create_log(
                evento="EMAIL_VERIFY_USED",
                ip_address=ip_address,
                user_agent=user_agent,
                exito=False,
            )
            raise ValueError("verification_link_used")

        if datetime.now() > token_obj.fecha_expiracion:
            self.security_log_repo.create_log(
                evento="EMAIL_VERIFY_EXPIRED",
                ip_address=ip_address,
                user_agent=user_agent,
                exito=False,
            )
            raise ValueError("verification_link_expired")

        usuario = self.usuario_repo.get_by_id(token_obj.usuario_id)
        if usuario is None:
            raise ValueError("user_not_found")

        actualizado = self.usuario_repo.mark_email_verified(usuario.id)
        if not actualizado:
            raise ValueError("email_verification_failed")

        marcado = self.verification_repo.mark_as_used(token_obj.id)
        if not marcado:
            raise ValueError("token_invalidation_failed")

        self.security_log_repo.create_log(
            evento="EMAIL_VERIFIED",
            ip_address=ip_address,
            user_agent=user_agent,
            exito=True,
        )

        return {"message": "email_verified"}
    
    def resend_verification_email(
        self,
        email: str,
        lang: str = "es",
        ip_address: str = "unknown",
        user_agent: str = "unknown",
    ):
        email = email.strip().lower()
        usuario = self.usuario_repo.get_by_email(email)

        if usuario is None or usuario.email_verificado:
            return {"message": "verification_email_resent"}

        ultimo_token = self.verification_repo.get_latest_by_user(usuario.id)
        
        if ultimo_token is not None:
            segundos_transcurridos = self.verification_repo.get_seconds_since_last_token(usuario.id)
            if segundos_transcurridos is not None and segundos_transcurridos < 180:
                segundos_restantes = max(1, int(180 - segundos_transcurridos))
                self.security_log_repo.create_log(
                    evento="EMAIL_VERIFY_RESEND_COOLDOWN",
                    email_intentado=email,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    exito=False,
                )
                raise ValueError(f"verification_resend_cooldown:{segundos_restantes}")

        token = secrets.token_urlsafe(32)
        fecha_expiracion = datetime.now() + timedelta(hours=24)

        self.verification_repo.invalidate_user_tokens(usuario.id)
        self.verification_repo.create_token(usuario.id, token, fecha_expiracion)

        verify_url = f"{settings.FRONTEND_URL}/verify-email/{token}"

        try:
            self.email_service.enviar_email_verificacion(
                destinatario=usuario.email,
                verify_url=verify_url,
                lang=lang,
            )
        except Exception:
            raise ValueError("verification_email_failed")

        self.security_log_repo.create_log(
            evento="EMAIL_VERIFY_RESENT",
            email_intentado=email,
            ip_address=ip_address,
            user_agent=user_agent,
            exito=True,
        )

        return {"message": "verification_email_resent"}