from app.services.sueno_service import SuenoService
from app.repositories.comentario_repository import ComentarioRepository
from app.services.notificacion_service import NotificacionService

class ComentarioService:
    def __init__(self,comentario_repository: ComentarioRepository ,sueno_service: SuenoService, notificacion_service: NotificacionService):
        self.comentario_repository = comentario_repository
        self.sueno_service = sueno_service
        self.notificacion_service = notificacion_service
        
        
    def create_comentario(self, contenido, usuario_id, sueno_id):
        #Validacion sueno
        sueno = self.sueno_service.get_sueno(sueno_id, usuario_id)
        #Limpieza contenido
        contenido = contenido.strip()
        #Validaciones comentario
        if not contenido:
            raise ValueError("Comentario vacio")
        if len(contenido)<2:
            raise ValueError("Comentario demasiado corto")
        if len(contenido)>500:
            raise ValueError("Comentario demasiado largo")
        
        comentario = self.comentario_repository.create(contenido,usuario_id, sueno_id)
        
        #Notificacion
        self.notificacion_service.crear_notificacion(
            usuario_id=sueno.usuario_id,
            tipo="comentario",
            emisor_id=usuario_id,
            sueno_id = sueno_id
        )
        
        return self.comentario_repository.get_detalle_by_id(comentario.id)
    
    def update_comentario(self, comentario_id, usuario_id, nuevo_comentario):
        #Validacion comentario
        comentario = self.comentario_repository.get_by_id(comentario_id)
        if not comentario:
            raise ValueError("Comentario no existe")
        #Validacion dueño
        if comentario.usuario_id != usuario_id:
            raise PermissionError("No autorizado")
        #Validacion nuevo comentario
        nuevo_comentario = nuevo_comentario.strip()
        if not nuevo_comentario:
            raise ValueError("Comentario vacio")
        if len(nuevo_comentario)<2:
            raise ValueError("Comentario demasiado corto")
        if len(nuevo_comentario)>500:
            raise ValueError("Comentario demasiado largo")
        
        self.comentario_repository.update(nuevo_comentario,comentario_id)
        
        return self.comentario_repository.get_detalle_by_id(comentario_id)
    
    def delete_comentario(self, comentario_id, usuario_id):
        #Validacion comentario
        comentario = self.comentario_repository.get_by_id(comentario_id)
        if not comentario:
            raise ValueError("Comentario no existe.")
        #Validacion sueño
        sueno = self.sueno_service.get_sueno(
            comentario.sueno_id,
            usuario_id
        )
        #Validacion autoria
        if (
            comentario.usuario_id != usuario_id
            and sueno.usuario_id != usuario_id
        ):
            raise PermissionError("No autorizado.")

        deleted = self.comentario_repository.delete(comentario_id)

        return deleted
    
    def get_comentarios_by_sueno(self, sueno_id, usuario_id):
        # Validar acceso al sueño
        self.sueno_service.get_sueno(sueno_id, usuario_id)

        return self.comentario_repository.get_detalle_by_sueno(sueno_id)