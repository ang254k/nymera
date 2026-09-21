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
                "message": "Si existe una cuenta asociada a ese correo, recibirás un email."
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
            "message": "Si existe una cuenta asociada a ese correo, recibirás un email."
        }

    def reset_password(self, token, new_password):
        token_obj = self.reset_repo.get_by_token(token)
        #Validaciones
        #Existe?
        if token_obj is None:
            raise ValueError("Token inválido")
        #Usado?
        if token_obj.usado:
            raise ValueError("Este enlace ya fue utilizado")
        #Fecha ok?
        if datetime.now() > token_obj.fecha_expiracion:
            raise ValueError("El enlace ha expirado")

        #Se busca usuario
        usuario = self.usuario_repo.get_by_id_with_password(token_obj.usuario_id)

        if usuario is None:
            raise ValueError("Usuario no encontrado")
        #Hash pw
        nuevo_hash = bcrypt.hash(new_password)
        #Actualiza usuario(pw)
        actualizado = self.usuario_repo.update_password(
            usuario.id,
            nuevo_hash
        )
        
        if not actualizado:
            raise ValueError("No se pudo actualizar la contraseña")
        #Se marca token
        marcado = self.reset_repo.mark_as_used(token_obj.id)
        
        if not marcado:
            raise ValueError("No se pudo invalidar el token")
        
        return{
            "message": "Contraseña actualizada correctamente"
        }