from fastapi import APIRouter, Depends, HTTPException, Query

from app.repositories.categoria_repository import CategoriaRepository
from app.repositories.sueno_repository import SuenoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.hashtag_repository import HashtagRepository

from app.services.sueno_service import SuenoService
from app.services.usuario_service import UsuarioService

from app.schemas.sueno_schema import SuenoFeedItem
from app.schemas.usuario_schema import PasswordUpdate, UsuarioUpdate, UsuarioResponse

from app.models.usuario import Usuario

from fastapi import UploadFile, File

from app.dependencies.auth import (
    get_current_user_optional, 
    get_current_user
)

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

sueno_service = SuenoService(
    SuenoRepository(),
    UsuarioRepository(),
    CategoriaRepository(),
    HashtagRepository()
)

usuario_service = UsuarioService(
    UsuarioRepository()
)

#Suenos de usuario
@router.get("/{id}/suenos", response_model= list[SuenoFeedItem])
def get_user_suenos(
    id: int,
    categorias: list[int] | None = Query(None),
    ordenar_por: str | None = None,
    direccion: str | None = None,
    current_user : Usuario | None = Depends(get_current_user_optional)
):
    usuario_actual_id = current_user.id if current_user else None
    
    try:
        return sueno_service.get_user_suenos(id, usuario_actual_id, categorias, ordenar_por, direccion)
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
#Editar perfil
@router.put("/me")
def update_me(
    data: UsuarioUpdate,
    current_user: Usuario = Depends(get_current_user)
):
    try:
        actualizado = usuario_service.update_user(
            current_user.id,
            nombre=data.nombre,
            current_password=data.current_password
        )

        if not actualizado:
            raise HTTPException(
                status_code=400,
                detail = "No se pudo actualizar el perfil"
            )
            
        return {
            "message": "Perfil actualizado correctamente"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@router.post("/me/avatar", response_model=UsuarioResponse)
def upload_avatar(
    avatar: UploadFile = File(...),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        return usuario_service.update_avatar(
                current_user.id,
                avatar
            )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.put("/me/password")
def change_password(
    data: PasswordUpdate,
    current_user: Usuario = Depends(get_current_user)
):
    try:
        actualizado = usuario_service.change_password(
            current_user.id,
            data.current_password,
            data.new_password
        )
        
        if not actualizado:
            raise HTTPException(
                status_code=400,
                detail="No se pudo actualizar la contraseña"
            )
        return {
            "message": "Contraseña actualizada correctamente"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/{id}", response_model=UsuarioResponse)
def get_usuario(id: int):
    usuario = usuario_service.get_user_by_id(id)
    
    if not usuario:
        raise HTTPException(
            status_code=404, 
            detail="Usuario no encontrado"
        )
    return usuario