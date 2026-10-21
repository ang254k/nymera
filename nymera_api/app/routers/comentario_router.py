from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth import get_current_user
from app.models.usuario import Usuario
from app.repositories.categoria_repository import CategoriaRepository
from app.repositories.comentario_repository import ComentarioRepository
from app.repositories.sueno_repository import SuenoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.hashtag_repository import HashtagRepository
from app.schemas.comentario_schema import (
    ComentarioResponse,
    ComentarioUpdateRequest,
    ComentarioDetalleResponse,
)
from app.services.comentario_service import ComentarioService
from app.services.sueno_service import SuenoService
from app.services.translation_service import TranslationService

from app.repositories.notificacion_repository import NotificacionRepository
from app.services.notificacion_service import NotificacionService

router = APIRouter(prefix="/comentarios", tags=["comentarios"])

sueno_service = SuenoService(
    SuenoRepository(),
    UsuarioRepository(),
    CategoriaRepository(),
    HashtagRepository(),
    TranslationService(),
)

notificacion_repository = NotificacionRepository()
notificacion_service = NotificacionService(notificacion_repository)

comentario_service = ComentarioService(
    ComentarioRepository(),
    sueno_service,
    notificacion_service,
    TranslationService()
)


# Modificar comentario
@router.put("/{id}", response_model=ComentarioDetalleResponse)
def update_comentario(
    id: int,
    data: ComentarioUpdateRequest,
    current_user: Usuario = Depends(get_current_user),
):
    try:
        comentario = comentario_service.update_comentario(
            comentario_id=id,
            usuario_id=current_user.id,
            nuevo_comentario=data.contenido,
        )
        return comentario

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


# Borrar comentario
@router.delete("/{id}", status_code=204)
def delete_comentario(id: int, current_user: Usuario = Depends(get_current_user)):
    try:
        comentario_service.delete_comentario(
            comentario_id=id, usuario_id=current_user.id
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


# Traducir comentario
@router.get("/{id}/traduccion")
def translate_comentario(
    id: int,
    idioma: str,
    current_user: Usuario | None = Depends(get_current_user),
):
    try:
        traduccion = comentario_service.translate_comentario(
            comentario_id=id,
            idioma_destino=idioma,
            usuario_actual_id=current_user.id,
        )
        return traduccion

    except ValueError as e:
        mensaje = str(e)

        if mensaje == "comment_not_found":
            raise HTTPException(status_code=404, detail=mensaje)

        raise HTTPException(status_code=400, detail=mensaje)

    except PermissionError:
        raise HTTPException(status_code=403, detail="unauthorized")
