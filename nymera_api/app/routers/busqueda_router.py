from fastapi import APIRouter, Depends, Query

from app.services.busqueda_service import BusquedaService
from app.dependencies.auth import get_current_user_optional

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)

busqueda_service = BusquedaService()


@router.get("")
def search(
    q: str,
    categorias: list[int] | None = Query(None),
    ordenar_por: str | None = None,
    direccion: str | None = None,
    current_user=Depends(get_current_user_optional),
):
    usuario_id = current_user.id if current_user else None

    return busqueda_service.search(
        q,
        usuario_id,
        categorias,
        ordenar_por,
        direccion,
    )
