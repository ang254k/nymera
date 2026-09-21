from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.sueno_repository import SuenoRepository
from app.repositories.hashtag_repository import HashtagRepository
from app.repositories.busqueda_repository import BusquedaRepository


class BusquedaService:

    def __init__(self):
        self.usuario_repository = UsuarioRepository()
        self.sueno_repository = SuenoRepository()
        self.hashtag_repository = HashtagRepository()
        self.busqueda_repository = BusquedaRepository()

    def search(
        self,
        termino,
        usuario_id,
        categorias=None,
        ordenar_por=None,
        direccion=None,
    ):
        # Busqueda hashtags
        if "#" in termino:

            hashtags = []
            # Extraccion hashtags
            for palabra in termino.split():

                if palabra.startswith("#"):
                    hashtags.append(palabra[1:].lower())

            suenos = self.busqueda_repository.get_suenos_by_hashtag(
                hashtags, usuario_id, categorias, ordenar_por, direccion
            )

            return {
                "usuarios": [],
                "suenos": [
                    {
                        "id": s.id,
                        "titulo": s.titulo,
                        "preview_contenido": s.preview_contenido,
                        "publico": s.publico,
                        "fecha_creacion": s.fecha_creacion,
                        "usuario_id": s.usuario_id,
                        "usuario_nombre": s.usuario_nombre,
                        "avatar_url": s.avatar_url,
                        "categoria_nombre": s.categoria_nombre,
                        "likes_count": s.likes_count,
                        "comentarios_count": s.comentarios_count,
                        "liked_by_user": s.liked_by_user,
                    }
                    for s in suenos
                ],
            }

        # Busqueda palabras
        palabras = termino.split()
        if len(palabras) > 1:

            suenos = self.busqueda_repository.get_suenos_multiple_words(
                palabras, usuario_id, categorias, ordenar_por, direccion
            )

            return {
                "usuarios": [],
                "suenos": [
                    {
                        "id": s.id,
                        "titulo": s.titulo,
                        "preview_contenido": s.preview_contenido,
                        "publico": s.publico,
                        "fecha_creacion": s.fecha_creacion,
                        "usuario_id": s.usuario_id,
                        "usuario_nombre": s.usuario_nombre,
                        "avatar_url": s.avatar_url,
                        "categoria_nombre": s.categoria_nombre,
                        "likes_count": s.likes_count,
                        "comentarios_count": s.comentarios_count,
                        "liked_by_user": s.liked_by_user,
                    }
                    for s in suenos
                ],
            }

        # Si no hay hashtags en la busqueda, buscamos usuarios y sueños
        usuarios = self.busqueda_repository.search_usuarios(termino)

        suenos = self.busqueda_repository.search_suenos(termino, usuario_id, categorias, ordenar_por, direccion)

        return {
            "usuarios": [
                {"id": u[0], "nombre": u[1], "avatar_url": u[2]} for u in usuarios
            ],
            "suenos": [
                {
                    "id": s.id,
                    "titulo": s.titulo,
                    "preview_contenido": s.preview_contenido,
                    "publico": s.publico,
                    "fecha_creacion": s.fecha_creacion,
                    "usuario_id": s.usuario_id,
                    "usuario_nombre": s.usuario_nombre,
                    "avatar_url": s.avatar_url,
                    "categoria_nombre": s.categoria_nombre,
                    "likes_count": s.likes_count,
                    "comentarios_count": s.comentarios_count,
                    "liked_by_user": s.liked_by_user,
                }
                for s in suenos
            ],
        }
