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
            raise ValueError("El email no tiene un formato válido")

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
            raise ValueError("El nombre no puede estar vacío")

        if len(nombre) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")

        if len(nombre) > 50:
            raise ValueError("El nombre es demasiado largo")

        # Validación email
        if not email:
            raise ValueError("El email no puede estar vacío")

        self._validar_email(email)

        # Validación contraseña
        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")

        if len(password) > 128:
            raise ValueError("La contraseña es demasiado larga")

        pw_hash = self._hash_password(password)

        return self.repo.insert(nombre, email, pw_hash)
    
    
    def update_user(self, user_id: int, nombre: str | None = None, current_password: str | None = None):
        usuario = self.repo.get_by_id_with_password(user_id)
        
        #Validación usuario
        if usuario is None:
            raise ValueError("Usuario no encontrado")
        
        #Validación pw's
        if current_password is None:
            raise ValueError("Debes introducir tu contraseña actual")
        
        if not bcrypt.verify(current_password, usuario.password):
            raise ValueError("Contraseña incorrecta")
        
        # Validación nombre
        if nombre is not None:
            nombre = nombre.strip()
            
            if len(nombre) < 3:
                raise ValueError("El nombre debe tener al menos 3 caracteres")
            if len(nombre) > 50:
                raise ValueError("El nombre es demasiado largo")
        
        actualizado = self.repo.update_perfil(
            user_id,
            nombre=nombre,
        )
        
        return actualizado
    
    def change_password(self, user_id: int, current_password: str, new_password: str):
        usuario = self.repo.get_by_id_with_password(user_id)
        
        if usuario is None:
            raise ValueError("Usuario no encontrado")
        
        if current_password is None:
            raise ValueError("Debes introducir tu contraseña actual")
        
        if not bcrypt.verify(current_password, usuario.password):
            raise ValueError("Contraseña actual incorrecta")
        
        if new_password is None:
            raise ValueError("Debes introducir una nueva contraseña")
        
        if len(new_password) < 8:
            raise ValueError("La nueva contraseña debe tener al menos 8 caracteres")
        
        if current_password == new_password:
            raise ValueError("La nueva contraseña debe ser distinta a la actual")
        
        nuevo_hash = bcrypt.hash(new_password)
        
        actualizado = self.repo.update_password(
            user_id,
            nuevo_hash,
        )
        
        if not actualizado:
            raise ValueError("No se pudo actualizar la contraseña")
        
        return actualizado
    
    def update_avatar(self, usuario_id, avatar: UploadFile):
        
        usuario = self.repo.get_by_id(usuario_id)
        
        if usuario is None:
            raise ValueError("Usuario no encontrado")
        
        if not avatar.filename:
            raise ValueError("Archivo inválido")
        
        #Comprobacion extension
        extension = avatar.filename.split(".")[-1].lower()
        
        if extension not in ["jpg", "jpeg", "png", "webp"]:
            raise ValueError(
                "Formato no permitido. Usa jpg, jpeg, png o webp"
            )
        
        nombre_archivo = f"{uuid.uuid4()}.{extension}"
        
        ruta_carpeta = "uploads/avatars"

        ruta_archivo = os.path.join(
            ruta_carpeta,
            nombre_archivo
        )
        
        contenido = avatar.file.read()
        
        #Validacion tamaño
        if len(contenido) > 5 * 1024 * 1024:
            raise ValueError("La imagen no puede superar los 5MB")
        
        #Validacion contenido = Imagen
        avatar.file.seek(0)
        
        try:
            imagen = Image.open(avatar.file)
            imagen.verify()
        except Exception:
            raise ValueError("El archivo no es una imagen válida")
        
        os.makedirs(
            ruta_carpeta,
            exist_ok=True
        )
        
        with open(ruta_archivo, "wb") as f:
            f.write(contenido)
            
        avatar_url = f"/uploads/avatars/{nombre_archivo}"
        
        actualizado = self.repo.update_avatar(
            usuario_id,
            avatar_url
        )
        
        #Borrado avatar anterior
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