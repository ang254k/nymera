from datetime import datetime

class Usuario:
    def __init__(
        self,
        id: int,
        nombre: str,
        email: str,
        password=None,
        fecha_creacion: datetime | None = None,
        avatar_url: str | None = None
    ):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.fecha_creacion = fecha_creacion
        self.avatar_url = avatar_url

    def __repr__(self):
        return f"Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')"