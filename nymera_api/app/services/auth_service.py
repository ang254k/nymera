from passlib.hash import bcrypt
from app.config import settings

from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.password_reset_repository import PasswordResetRepository
from app.services.email_service import EmailService

from datetime import datetime, timedelta
import secrets


class AuthService:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
        self.reset_repo = PasswordResetRepository()
        self.email_service = EmailService()

    def forgot_password(self, email):
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
        )

        return {
            "message": "password_reset_email_sent"
        }

    def reset_password(self, token, new_password):
        token_obj = self.reset_repo.get_by_token(token)
        #Validaciones
        #Existe?
        if token_obj is None:
            raise ValueError("token_invalid")
        #Usado?
        if token_obj.usado:
            raise ValueError("reset_link_used")
        #Fecha ok?
        if datetime.now() > token_obj.fecha_expiracion:
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