# Se cre esta clase para no mezclar información con modelo Comentario
class ComentarioDetalle:
    def __init__(self, id, contenido, fecha_creacion, usuario_id, usuario_nombre, avatar_url):
        self.id = id
        self.contenido = contenido
        self.fecha_creacion = fecha_creacion
        self.usuario_id = usuario_id
        self.usuario_nombre = usuario_nombre
        self.avatar_url = avatar_url
        

    def __repr__(self):
        return (
            f"ComentarioDetalle("
            f"id={self.id}, "
            f"fecha_creacion={self.fecha_creacion})"
            f"usuario_id={self.usuario_id}, "
            f"usuario_nombre={self.usuario_nombre}, "
        )
