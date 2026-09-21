from pydantic import BaseModel
from datetime import datetime

class NotificacionOut(BaseModel):
    id: int
    tipo: str
    emisor_nombre: str | None
    sueno_id: int | None
    leido: bool
    fecha_creacion: datetime