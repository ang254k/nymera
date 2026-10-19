class SuenoFeedDetalle:
    def __init__(
        self,
        id,
        titulo,
        preview_contenido,
        publico,
        fecha_creacion,
        usuario_id: int,
        idioma_original,
        usuario_nombre,
        avatar_url,
        categoria_id,
        categoria_nombre,
        likes_count,
        comentarios_count,
        liked_by_user,
    ):
        self.id = id
        self.titulo = titulo
        self.preview_contenido = preview_contenido
        self.publico = publico
        self.fecha_creacion = fecha_creacion
        self.usuario_id = usuario_id
        self.idioma_original = idioma_original
        self.usuario_nombre = usuario_nombre
        self.avatar_url = avatar_url
        self.categoria_id = categoria_id
        self.categoria_nombre = categoria_nombre
        self.likes_count = likes_count
        self.comentarios_count = comentarios_count
        self.liked_by_user = liked_by_user
