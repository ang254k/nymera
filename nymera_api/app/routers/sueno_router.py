from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.sueno_schema import (
    SuenoCreateRequest,
    SuenoResponse,
    SuenoDetalleResponse,
    SuenoUpdateRequest,
    SuenoFeedItem,
)
from app.schemas.comentario_schema import (
    ComentarioDetalleResponse,
    ComentarioResponse,
    ComentarioCreateRequest,
)
from app.schemas.like_schema import LikeResponse

from app.services.sueno_service import SuenoService
from app.services.like_service import LikeService
from app.services.comentario_service import ComentarioService
from app.services.notificacion_service import NotificacionService

from app.repositories.like_repository import LikeRepository
from app.repositories.sueno_repository import SuenoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.categoria_repository import CategoriaRepository
from app.repositories.comentario_repository import ComentarioRepository
from app.repositories.hashtag_repository import HashtagRepository
from app.repositories.notificacion_repository import NotificacionRepository

from app.dependencies.auth import get_current_user, get_current_user_optional
from app.models.usuario import Usuario

router = APIRouter(prefix="/suenos", tags=["suenos"])

sueno_service = SuenoService(
    SuenoRepository(), UsuarioRepository(), CategoriaRepository(), HashtagRepository()
)

notificacion_repository = NotificacionRepository()
notificacion_service = NotificacionService(notificacion_repository)

comentario_service = ComentarioService(
    ComentarioRepository(), sueno_service, notificacion_service
)

like_service = LikeService(LikeRepository(), sueno_service, notificacion_service)


# Crear Sueno
@router.post("", response_model=SuenoFeedItem)
def create_sueno(
    data: SuenoCreateRequest, current_user: Usuario = Depends(get_current_user)
):
    try:
        sueno = sueno_service.create_sueno(
            titulo=data.titulo,
            contenido=data.contenido,
            usuario_id=current_user.id,
            categoria_id=data.categoria_id,
            publico=data.publico,
        )

        return sueno

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Editar Sueno
@router.put("/{id}", response_model=SuenoResponse)
def update_sueno(
    data: SuenoUpdateRequest, id: int, current_user: Usuario = Depends(get_current_user)
):
    try:
        sueno = sueno_service.update_sueno(
            sueno_id=id,
            titulo=data.titulo,
            contenido=data.contenido,
            categoria_id=data.categoria_id,
            publico=data.publico,
            usuario_actual_id=current_user.id,
        )

        return sueno

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except PermissionError:
        raise HTTPException(status_code=403, detail="unauthorized")


# Borrar Sueno
@router.delete("/{id}", status_code=204)
def delete_sueno(id: int, current_user: Usuario = Depends(get_current_user)):
    try:
        sueno_service.delete_sueno(sueno_id=id, usuario_actual_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except PermissionError:
        raise HTTPException(status_code=403, detail="unauthorized")


# Sueno por id
@router.get("/{id}", response_model=SuenoDetalleResponse)
def get_sueno(
    id: int, current_user: Usuario | None = Depends(get_current_user_optional)
):
    usuario_actual_id = current_user.id if current_user else None

    return sueno_service.get_sueno_detalles(id, usuario_actual_id)


# Comentarios de sueno
@router.get("/{id}/comentarios", response_model=list[ComentarioDetalleResponse])
def get_comentarios(
    id: int, current_user: Usuario | None = Depends(get_current_user_optional)
):
    usuario_actual_id = current_user.id if current_user else None

    return comentario_service.get_comentarios_by_sueno(id, usuario_actual_id)


# Like de Sueno
@router.post("/{id}/like", response_model=LikeResponse)
def toggle_like(id: int, current_user: Usuario = Depends(get_current_user)):
    return like_service.toggle_like(id, current_user.id)


# Crear comentario
@router.post("/{id}/comentarios", response_model=ComentarioDetalleResponse)
def create_comentario(
    id: int,
    data: ComentarioCreateRequest,
    current_user: Usuario = Depends(get_current_user),
):
    try:
        comentario = comentario_service.create_comentario(
            contenido=data.contenido, usuario_id=current_user.id, sueno_id=id
        )
        return comentario

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except PermissionError:
        raise HTTPException(status_code=403, detail="unauthorized")


# Sueños likeados por usuario
@router.get("/usuarios/{id}/likes", response_model=list[SuenoFeedItem])
def get_liked_suenos(
    id: int,
    categorias: list[int] | None = Query(None),
    ordenar_por: str | None = None,
    direccion: str | None = None,
    current_user: Usuario = Depends(get_current_user),
):
    if current_user.id != id:
        raise HTTPException(status_code=403, detail="unauthorized")

    return sueno_service.get_liked_suenos(
        id, current_user.id, categorias, ordenar_por, direccion
    )

