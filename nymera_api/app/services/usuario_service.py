import cloudinary.uploader
import re
import os
import uuid
import io

from PIL import Image
from fastapi import UploadFile
from passlib.hash import bcrypt
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.security_log_repository import SecurityLogRepository

class UsuarioService:

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo
        self.security_log_repo = SecurityLogRepository()

    def _hash_password(self, password: str) -> str:
        return bcrypt.hash(password)

    def _validar_email(self, email: str):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            raise ValueError("email_invalid")

    def login(self, email: str, password: str, ip_address: str = "unknown", user_agent: str = "unknown") -> Usuario | None:
        email = email.strip().lower()

        usuario = self.repo.get_by_email(email)

        if usuario is None:
            self.security_log_repo.create_log(
                evento="LOGIN_FAILED",
                email_intentado=email,
                ip_address=ip_address,
                user_agent=user_agent,
                exito=False
            )
            return None

        if bcrypt.verify(password, usuario.password):
            return usuario
        
        #Si la contraseña es incorrecta, registramos
        self.security_log_repo.create_log(
            evento="LOGIN_FAILED",
            email_intentado=email,
            ip_address=ip_address,
            user_agent=user_agent,
            exito=False
        )
        return None

    def register(self, nombre: str, email: str, password: str) -> Usuario:

        nombre = nombre.strip()
        email = email.strip().lower()
        password = password.strip()

        # Validación nombre
        if not nombre:
            raise ValueError("name_empty")

        if len(nombre) < 3:
            raise ValueError("name_too_short")

        if len(nombre) > 50:
            raise ValueError("name_too_long")

        # Validación email
        if not email:
            raise ValueError("email_empty")

        self._validar_email(email)

        # Validación contraseña
        if len(password) < 8:
            raise ValueError("password_too_short")

        if len(password) > 128:
            raise ValueError("password_too_long")

        pw_hash = self._hash_password(password)

        return self.repo.insert(nombre, email, pw_hash)

    def update_user(
        self,
        user_id: int,
        nombre: str | None = None,
        current_password: str | None = None,
    ):
        usuario = self.repo.get_by_id_with_password(user_id)

        # Validación usuario
        if usuario is None:
            raise ValueError("user_not_found")

        # Validación pw's
        if current_password is None:
            raise ValueError("current_password_required")

        if not bcrypt.verify(current_password, usuario.password):
            raise ValueError("password_incorrect")

        # Validación nombre
        if nombre is not None:
            nombre = nombre.strip()

            if not nombre:
                raise ValueError("name_empty")
            if len(nombre) < 3:
                raise ValueError("name_too_short")
            if len(nombre) > 50:
                raise ValueError("name_too_long")

        actualizado = self.repo.update_perfil(
            user_id,
            nombre=nombre,
        )

        return actualizado

    def change_password(self, user_id: int, current_password: str, new_password: str):
        usuario = self.repo.get_by_id_with_password(user_id)

        if usuario is None:
            raise ValueError("user_not_found")

        if current_password is None:
            raise ValueError("current_password_required")

        if not bcrypt.verify(current_password, usuario.password):
            raise ValueError("current_password_incorrect")

        if new_password is None:
            raise ValueError("new_password_required")

        if len(new_password) < 8:
            raise ValueError("new_password_too_short")

        if current_password == new_password:
            raise ValueError("new_password_same")

        nuevo_hash = bcrypt.hash(new_password)

        actualizado = self.repo.update_password(
            user_id,
            nuevo_hash,
        )

        if not actualizado:
            raise ValueError("password_update_failed")

        return actualizado

    def update_avatar(self, usuario_id, avatar: UploadFile):
        usuario = self.repo.get_by_id(usuario_id)

        if usuario is None:
            raise ValueError("user_not_found")

        if not avatar.filename:
            raise ValueError("file_invalid")

        # Comprobacion extension
        extension = avatar.filename.split(".")[-1].lower()

        if extension not in ["jpg", "jpeg", "png", "webp"]:
            raise ValueError("image_format_invalid")

        contenido = avatar.file.read()

        # Validacion tamaño
        if len(contenido) > 5 * 1024 * 1024:
            raise ValueError("image_too_large")

        # Validacion contenido = Imagen
        avatar.file.seek(0)

        try:
            imagen = Image.open(io.BytesIO(contenido))
            imagen.verify()
        except Exception:
            raise ValueError("image_invalid")

        try:          
            cloudinary.config(
                cloudinary_url=os.getenv("CLOUDINARY_URL"),
                secure=True
            )  
            
            upload_result = cloudinary.uploader.upload(
                contenido,
                folder="nymera_avatars",
                public_id=f"user_{usuario_id}",
                overwrite=True,
                resource_type="image"
            )
            avatar_url = upload_result.get("secure_url")
        except Exception as e:
            print(f"Error en Cloudinary: {e}")
            raise ValueError("cloud_upload_failed")
        
        actualizado = self.repo.update_avatar(usuario_id, avatar_url)

        return actualizado

    def get_user_by_id(self, user_id):
        return self.repo.get_by_id(user_id)

    def delete_account(self, user_id: int, current_password: str) -> bool:
        usuario = self.repo.get_by_id_with_password(user_id)

        if usuario is None:
            raise ValueError("user_not_found")

        if current_password is None:
            raise ValueError("current_password_required")

        if not bcrypt.verify(current_password, usuario.password):
            raise ValueError("current_password_incorrect")

        #Borrado avatar usuario
        try:
            cloudinary.config(
                cloudinary_url=os.getenv("CLOUDINARY_URL"),
                secure=True
            )
            cloudinary.uploader.destroy(f"nymera_avatars/user_{user_id}")
        except Exception:
            pass

        eliminado = self.repo.delete(user_id)

        if not eliminado:
            raise ValueError("user_delete_failed")

        return True