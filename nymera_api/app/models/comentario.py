class Comentario:
    def __init__(self, id, contenido, fecha_creacion, usuario_id, sueno_id):
        self.id = id
        self.contenido = contenido
        self.fecha_creacion = fecha_creacion
        self.usuario_id = usuario_id
        self.sueno_id = sueno_id
        
    def __repr__(self):
        return(
            f"Comentario(id={self.id}, usuario_id={self.usuario_id}, "
            f"sueno_id={self.sueno_id})"
        )