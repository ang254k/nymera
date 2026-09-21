class Sueno:
    def __init__(self, id, titulo, contenido, publico, fecha_creacion, usuario_id: int | None, categoria_id):
        self.id = id
        self.titulo = titulo
        self.contenido = contenido
        self.publico = publico
        self.fecha_creacion = fecha_creacion
        self.usuario_id = usuario_id
        self.categoria_id = categoria_id

    def __repr__(self):
        return (
            f"Sueno(id={self.id}, titulo='{self.titulo}', "
            f"usuario_id={self.usuario_id}, categoria_id={self.categoria_id})"
        )