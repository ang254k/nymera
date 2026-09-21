from app.repositories.notificacion_repository import NotificacionRepository

class NotificacionService:

    def __init__(self, notificacion_repository: NotificacionRepository):
        self.notificacion_repository = notificacion_repository

    def crear_notificacion(self, usuario_id, tipo, emisor_id, sueno_id):
        # evitar auto-notificaciones
        if usuario_id == emisor_id:
            return

        self.notificacion_repository.create(
            usuario_id,
            tipo,
            emisor_id,
            sueno_id
        )
        
    def get_by_user(self, usuario_id):
        return self.notificacion_repository.get_by_user(usuario_id)
    
    def marcar_como_leida(self, notificacion_id, usuario_id):
        self.notificacion_repository.marcar_como_leida(
            notificacion_id,
            usuario_id
        )