from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


#Peticiones
class ComentarioCreateRequest(BaseModel):
    contenido: str = Field(min_length= 2, max_length= 500)

class ComentarioUpdateRequest(BaseModel):
    contenido: str = Field(min_length= 2, max_length= 500)
    
#Respuestas
class ComentarioDetalleResponse(BaseModel):
    id: int
    contenido: str
    fecha_creacion: datetime
    usuario_id: int
    usuario_nombre: str
    avatar_url: str | None = None
    
    model_config = ConfigDict(from_attributes=True)


#Creo que no se usará pero se deja por si acaso
class ComentarioResponse(BaseModel):
    id: int
    contenido: str
    fecha_creacion: datetime
    usuario_id: int
    sueno_id: int
    #Para convertir de objeto a schema:
    model_config = ConfigDict(from_attributes=True)
