import re
import os
import uuid

from PIL import Image
from fastapi import UploadFile
from passlib.hash import bcrypt
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository


class UsuarioService:

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def _hash_password(self, password: str) -> str:
        return bcrypt.hash(password)

    def _validar_email(self, email: str):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            raise ValueError("email_invalid")

    def login(self, email: str, password: str) -> Usuario | None:
        email = email.strip().lower()

        usuario = self.repo.get_by_email(email)

        if usuario is None:
            return None

        if bcrypt.verify(password, usuario.password):
            return usuario

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

        nombre_archivo = f"{uuid.uuid4()}.{extension}"

        ruta_carpeta = "uploads/avatars"

        ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)

        contenido = avatar.file.read()

        # Validacion tamaño
        if len(contenido) > 5 * 1024 * 1024:
            raise ValueError("image_too_large")

        # Validacion contenido = Imagen
        avatar.file.seek(0)

        try:
            imagen = Image.open(avatar.file)
            imagen.verify()
        except Exception:
            raise ValueError("image_invalid")

        os.makedirs(ruta_carpeta, exist_ok=True)

        with open(ruta_archivo, "wb") as f:
            f.write(contenido)

        avatar_url = f"/uploads/avatars/{nombre_archivo}"

        actualizado = self.repo.update_avatar(usuario_id, avatar_url)

        # Borrado avatar anterior
        if usuario.avatar_url:
            ruta_anterior = usuario.avatar_url.lstrip("/")

            try:
                if os.path.exists(ruta_anterior):
                    os.remove(ruta_anterior)
            except OSError:
                pass

        return actualizado

    def get_user_by_id(self, user_id):
        return self.repo.get_by_id(user_id)
