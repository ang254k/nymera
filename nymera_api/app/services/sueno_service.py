from app.models.sueno import Sueno
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.sueno_repository import SuenoRepository
from app.repositories.categoria_repository import CategoriaRepository
from app.repositories.hashtag_repository import HashtagRepository

import re


class SuenoService:

    def __init__(
        self,
        sueno_repository: SuenoRepository,
        usuario_repository: UsuarioRepository,
        categoria_repository: CategoriaRepository,
        hashtag_repository: HashtagRepository,
    ):
        self.sueno_repository = sueno_repository
        self.usuario_repository = usuario_repository
        self.categoria_repository = categoria_repository
        self.hashtag_repository = hashtag_repository

    def create_sueno(self, titulo, contenido, usuario_id, categoria_id, publico=True):

        usuario = self.usuario_repository.get_by_id(usuario_id)
        categoria = self.categoria_repository.get_by_id(categoria_id)

        if not titulo or titulo.strip() == "":
            raise ValueError("title_empty")

        if len(titulo.strip()) < 3:
            raise ValueError("title_too_short")

        if len(titulo.strip()) > 100:
            raise ValueError("title_too_long")
        if not categoria:
            raise ValueError("category_not_found")
        if not usuario:
            raise ValueError("user_does_not_exist")

        if not contenido or len(contenido.strip()) < 5:
            raise ValueError("content_too_short")

        if len(contenido.strip()) > 2000:
            raise ValueError("content_too_long")
        
        sueno = self.sueno_repository.create(
            titulo, contenido, usuario_id, categoria_id, publico
        )

        # Despues de crear el sueño, se extraen los posibles hashtags
        hashtags = self.extract_hashtags(titulo + " " + contenido)

        for nombre in hashtags:
            hashtag = self.hashtag_repository.get_by_nombre(nombre)
            # Si no está en la lista, se añade
            if hashtag is None:
                hashtag = self.hashtag_repository.insert(nombre)

            self.hashtag_repository.insert_sueno_hashtag(sueno.id, hashtag.id)

        return self.sueno_repository.get_feed_item_by_id(
            sueno.id,
            usuario_id,
        )

    def update_sueno(
        self, sueno_id, titulo, contenido, categoria_id, publico, usuario_actual_id
    ):
        # Validación sueño
        sueno = self.sueno_repository.get_by_id(sueno_id)
        if not sueno:
            raise ValueError("dream_not_found")

        # Validación autoría
        if sueno.usuario_id != usuario_actual_id:
            raise PermissionError("unauthorized")

        # Validación categoría
        categoria = self.categoria_repository.get_by_id(categoria_id)
        if not categoria:
            raise ValueError("category_not_found")

        # Validación titulo
        if not titulo or titulo.strip() == "":
            raise ValueError("title_empty")

        if len(titulo.strip()) < 3:
            raise ValueError("title_too_short")

        if len(titulo.strip()) > 100:
            raise ValueError("title_too_long")
        
        # Validación contenido
        if not contenido or len(contenido.strip()) < 5:
            raise ValueError("content_too_short")

        if len(contenido.strip()) > 2000:
            raise ValueError("content_too_long")

        sueno_actualizado = self.sueno_repository.update(
            sueno_id, titulo, contenido, categoria_id, publico
        )

        # Eliminar relaciones hashtags antiguas
        self.hashtag_repository.delete_relaciones_sueno(sueno_id)

        # Extraer hashtags nuevos
        hashtags = self.extract_hashtags(titulo + " " + contenido)

        for nombre in hashtags:

            hashtag = self.hashtag_repository.get_by_nombre(nombre)

            if hashtag is None:
                hashtag = self.hashtag_repository.insert(nombre)

            self.hashtag_repository.insert_sueno_hashtag(sueno_id, hashtag.id)

        return sueno_actualizado

    def delete_sueno(self, sueno_id, usuario_actual_id):
        # Validacion sueño
        sueno = self.sueno_repository.get_by_id(sueno_id)
        if not sueno:
            raise ValueError("dream_not_found")
        # Validación autoría
        if sueno.usuario_id != usuario_actual_id:
            raise PermissionError("unauthorized")

        return self.sueno_repository.delete(sueno_id)

    def get_sueno_detalles(self, sueno_id, usuario_actual_id=None):
        # Validacion Sueno
        sueno = self.sueno_repository.get_detalles(usuario_actual_id, sueno_id)
        if not sueno:
            raise ValueError("dream_not_found")
        if not sueno.publico:
            if usuario_actual_id != sueno.usuario_id:
                raise PermissionError("unauthorized")
        return sueno

    def get_sueno(self, sueno_id, usuario_actual_id=None):
        sueno = self.sueno_repository.get_by_id(sueno_id)
        if not sueno:
            raise ValueError("dream_not_found")
        if not sueno.publico:
            if usuario_actual_id != sueno.usuario_id:
                raise PermissionError("unauthorized")
        return sueno

    def get_user_suenos(
        self,
        perfil_usuario_id,
        usuario_actual_id=None,
        categorias=None,
        ordenar_por=None,
        direccion=None,
    ):

        usuario = self.usuario_repository.get_by_id(perfil_usuario_id)

        if not usuario:
            raise ValueError("user_does_not_exist")

        return self.sueno_repository.get_feed_by_user(
            perfil_usuario_id, usuario_actual_id, categorias, ordenar_por, direccion
        )

    def get_feed(
        self, usuario_id=None, page=1, categorias=None, ordenar_por=None, direccion=None
    ):

        if page < 1:
            raise ValueError("page_invalid")

        PAGE_SIZE = 20
        # Se salta el numero de página que se selecciona, por la cantidad de contenido, en este caso 20

        offset = (page - 1) * PAGE_SIZE

        return self.sueno_repository.get_feed_detalle(
            usuario_id, PAGE_SIZE, offset, categorias, ordenar_por, direccion
        )

    def get_liked_suenos(
        self,
        perfil_usuario_id,
        usuario_actual_id=None,
        categorias=None,
        ordenar_por=None,
        direccion=None,
    ):
        usuario = self.usuario_repository.get_by_id(perfil_usuario_id)

        if not usuario:
            raise ValueError("user_does_not_exist")

        return self.sueno_repository.get_liked_by_user(
            perfil_usuario_id, usuario_actual_id, categorias, ordenar_por, direccion
        )

    def extract_hashtags(self, contenido: str):
        return list(set(re.findall(r"#([a-zA-Z0-9_áéíóúñÁÉÍÓÚÑ]+)", contenido.lower())))
