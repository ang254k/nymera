class NotificacionDetalle:
    def __init__(
        self,
        id,
        tipo,
        emisor_nombre,
        sueno_id,
        leido,
        fecha_creacion
    ):
        self.id = id
        self.tipo = tipo
        self.emisor_nombre = emisor_nombre
        self.sueno_id = sueno_id
        self.leido = leido
        self.fecha_creacion = fecha_creacion