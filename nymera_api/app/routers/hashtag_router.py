from fastapi import APIRouter, Depends, HTTPException, Query

from app.services.hashtag_service import HashtagService
from app.dependencies.auth import get_current_user_optional

router = APIRouter(prefix="/hashtags", tags=["hashtags"])

hashtag_service = HashtagService()


@router.get("/trending")
def get_trending():
    return hashtag_service.get_trending()


# Sueños de X hashtag
@router.get("/{nombre}")
def get_hashtag_suenos(
    nombre: str,
    categorias: list[int] | None = Query(None),
    ordenar_por: str | None = None,
    direccion: str | None = None,
    current_user=Depends(get_current_user_optional),
):
    usuario_id = current_user.id if current_user else None

    try:
        return hashtag_service.get_suenos_by_hashtag(
            nombre,
            usuario_id,
            categorias,
            ordenar_por,
            direccion,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
