from fastapi import APIRouter, Depends
from app.schemas.notificacion_schema import NotificacionOut
from app.dependencies.auth import get_current_user
from app.models.usuario import Usuario
from app.repositories.notificacion_repository import NotificacionRepository
from app.services.notificacion_service import NotificacionService

router = APIRouter(
    prefix = "/notificaciones",
    tags = ["notificaciones"]
)

notificacion_repository = NotificacionRepository()
notificacion_service = NotificacionService(notificacion_repository)

@router.get("/", response_model=list[NotificacionOut])
def get_notificaciones(current_user: Usuario = Depends(get_current_user)):
    return notificacion_service.get_by_user(current_user.id)

@router.put("/{id}/leer")
def marcar_leida(
    id: int,
    current_user: Usuario = Depends(get_current_user)
):
    notificacion_service.marcar_como_leida(id, current_user.id)
    return {"ok": True}