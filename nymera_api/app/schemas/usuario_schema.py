from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    fecha_creacion: datetime | None = None
    avatar_url: str | None = None
    
    model_config = ConfigDict(from_attributes=True)

class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    current_password: str | None = None
    
class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)