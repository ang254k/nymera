from fastapi import APIRouter
from app.repositories.categoria_repository import CategoriaRepository
from app.schemas.categoria_schema import CategoriaResponse

router = APIRouter(
    prefix="/categorias",
    tags=["categorias"]
)

repo = CategoriaRepository()

@router.get("", response_model= list[CategoriaResponse])
def get_categorias():
    return repo.get_all()