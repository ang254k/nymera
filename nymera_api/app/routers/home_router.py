from fastapi import APIRouter, Depends, Query
from app.schemas.sueno_schema import SuenoFeedItem
from app.services.sueno_service import SuenoService
from app.dependencies.auth import get_current_user_optional
from app.models.usuario import Usuario
from app.repositories.sueno_repository import SuenoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.categoria_repository import CategoriaRepository
from app.repositories.hashtag_repository import HashtagRepository

#No se añade prefijo para que sea /home
router = APIRouter(
    tags=["home"]
)
sueno_service = SuenoService(
    SuenoRepository(),
    UsuarioRepository(),
    CategoriaRepository(),
    HashtagRepository()
)
@router.get("/home", response_model=list[SuenoFeedItem])
def get_feed(
    page: int = 1,
    categorias: list[int] | None = Query(None),
    ordenar_por: str | None = None,
    direccion: str | None = None,
    current_user: Usuario | None = Depends(get_current_user_optional)
):
    usuario_id = current_user.id if current_user else None

    return sueno_service.get_feed(usuario_id, page, categorias, ordenar_por, direccion)

