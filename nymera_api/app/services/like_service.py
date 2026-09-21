
from app.repositories.like_repository import LikeRepository
from app.services.sueno_service import SuenoService
from app.services.notificacion_service import NotificacionService

class LikeService:
    def __init__(self, like_repository :LikeRepository, sueno_service: SuenoService, notificacion_service: NotificacionService):
        self.like_repository = like_repository
        self.sueno_service = sueno_service
        self.notificacion_service = notificacion_service
    
    def toggle_like(self, sueno_id, usuario_id):
        #Verificacion del sueño
        sueno = self.sueno_service.get_sueno(sueno_id, usuario_id)
        
        #Logica like-unlike
        liked = self.like_repository.exists(usuario_id, sueno_id)
        
        if liked:
            self.like_repository.remove_like(usuario_id, sueno_id)
            status = "unliked"
        else:
            self.like_repository.add_like(usuario_id, sueno_id)
            status = "liked"
            
            #Se crea la notificacion solo cuando hay Like
            if sueno.usuario_id != usuario_id:
                self.notificacion_service.crear_notificacion(
                    usuario_id = sueno.usuario_id,
                    tipo = "like",
                    emisor_id = usuario_id,
                    sueno_id = sueno_id
                )

        likes_count = self.like_repository.count_by_sueno(sueno_id)

        return {
            "status": status,
            "likes_count": likes_count
        }