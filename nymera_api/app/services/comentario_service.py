from app.services.sueno_service import SuenoService
from app.services.translation_service import TranslationService
from app.repositories.comentario_repository import ComentarioRepository
from app.services.notificacion_service import NotificacionService


class ComentarioService:
    def __init__(
        self,
        comentario_repository: ComentarioRepository,
        sueno_service: SuenoService,
        notificacion_service: NotificacionService,
        translation_service: TranslationService,
    ):
        self.comentario_repository = comentario_repository
        self.sueno_service = sueno_service
        self.notificacion_service = notificacion_service
        self.translation_service = translation_service

    def create_comentario(self, contenido, usuario_id, sueno_id, idioma_original="es"):
        # Validacion sueno
        sueno = self.sueno_service.get_sueno(sueno_id, usuario_id)
        # Limpieza contenido
        contenido = contenido.strip()
        # Validaciones comentario
        if not contenido:
            raise ValueError("comment_empty")
        if len(contenido) < 2:
            raise ValueError("comment_too_short")
        if len(contenido) > 500:
            raise ValueError("comment_too_long")
        if idioma_original not in ("es", "en"):
            raise ValueError("invalid_language")
        comentario = self.comentario_repository.create(
            contenido, usuario_id, sueno_id, idioma_original
        )

        # Notificacion
        self.notificacion_service.crear_notificacion(
            usuario_id=sueno.usuario_id,
            tipo="comentario",
            emisor_id=usuario_id,
            sueno_id=sueno_id,
        )

        return self.comentario_repository.get_detalle_by_id(comentario.id)

    def update_comentario(self, comentario_id, usuario_id, nuevo_comentario):
        # Validacion comentario
        comentario = self.comentario_repository.get_by_id(comentario_id)
        if not comentario:
            raise ValueError("comment_not_found")
        # Validacion dueño
        if comentario.usuario_id != usuario_id:
            raise PermissionError("unauthorized")
        # Validacion nuevo comentario
        nuevo_comentario = nuevo_comentario.strip()
        if not nuevo_comentario:
            raise ValueError("comment_empty")
        if len(nuevo_comentario) < 2:
            raise ValueError("comment_too_short")
        if len(nuevo_comentario) > 500:
            raise ValueError("comment_too_long")

        self.comentario_repository.update(nuevo_comentario, comentario_id)

        # Borrar traducciones antiguas
        self.comentario_repository.delete_traducciones(comentario_id)

        return self.comentario_repository.get_detalle_by_id(comentario_id)

    def delete_comentario(self, comentario_id, usuario_id):
        # Validacion comentario
        comentario = self.comentario_repository.get_by_id(comentario_id)
        if not comentario:
            raise ValueError("comment_not_found")
        # Validacion sueño
        sueno = self.sueno_service.get_sueno(comentario.sueno_id, usuario_id)
        # Validacion autoria
        if comentario.usuario_id != usuario_id and sueno.usuario_id != usuario_id:
            raise PermissionError("unauthorized")

        deleted = self.comentario_repository.delete(comentario_id)

        return deleted

    def get_comentarios_by_sueno(self, sueno_id, usuario_id):
        # Validar acceso al sueño
        self.sueno_service.get_sueno(sueno_id, usuario_id)

        return self.comentario_repository.get_detalle_by_sueno(sueno_id)

    def translate_comentario(
        self,
        comentario_id,
        idioma_destino,
        usuario_actual_id,
    ):
        # Validar comentario
        comentario = self.comentario_repository.get_by_id(comentario_id)

        if not comentario:
            raise ValueError("comment_not_found")

        # Validar acceso al sueño
        self.sueno_service.get_sueno(
            comentario.sueno_id,
            usuario_actual_id,
        )

        # Validar idioma
        if idioma_destino not in ("es", "en"):
            raise ValueError("invalid_language")

        if idioma_destino == comentario.idioma_original:
            raise ValueError("same_language")

        # Consultar traducción guardada
        traduccion = self.comentario_repository.get_traduccion(
            comentario_id,
            idioma_destino,
        )

        if traduccion is None:
            # Traducir comentario
            contenido = self.translation_service.translate(
                comentario.contenido,
                comentario.idioma_original,
                idioma_destino,
            )

            # Guardar traducción
            traduccion = self.comentario_repository.save_traduccion(
                comentario_id,
                idioma_destino,
                contenido,
            )

        return {
            "idioma": idioma_destino,
            "contenido": traduccion,
        }