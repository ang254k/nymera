class Notificacion:
    def __init__(
        self,
        id,
        usuario_id,
        tipo,
        emisor_id,
        sueno_id,
        leido,
        fecha_creacion
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.tipo = tipo
        self.emisor_id = emisor_id
        self.sueno_id = sueno_id
        self.leido = leido
        self.fecha_creacion = fecha_creacion