
from pydantic import BaseModel, ConfigDict
from datetime import datetime

#Peticiones
class SuenoCreateRequest(BaseModel):
    titulo: str
    contenido: str
    publico: bool
    categoria_id:int
    
class SuenoUpdateRequest(BaseModel):
    titulo: str
    contenido: str 
    publico: bool
    categoria_id: int
    
#Respuestas
class SuenoResponse(BaseModel):
    id: int
    titulo: str
    contenido: str
    publico: bool
    fecha_creacion: datetime
    usuario_id: int
    categoria_id: int
    
    model_config = ConfigDict(from_attributes=True)

class SuenoFeedItem(BaseModel):
    id: int
    titulo: str
    preview_contenido: str
    publico: bool
    fecha_creacion: datetime
    usuario_id: int
    usuario_nombre: str
    avatar_url: str | None = None
    categoria_nombre: str
    likes_count: int
    comentarios_count: int
    liked_by_user: bool
    
    model_config = ConfigDict(from_attributes=True)

class SuenoDetalleResponse(BaseModel):
    id: int
    titulo: str
    contenido: str
    fecha_creacion: datetime
    usuario_id: int
    usuario_nombre: str
    avatar_url: str | None = None
    likes_count: int
    comentarios_count: int
    liked_by_user: bool
    publico: bool
    categoria_id: int
    categoria_nombre: str
    

    model_config = ConfigDict(from_attributes=True)