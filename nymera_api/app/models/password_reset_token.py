class PasswordResetToken:
    def __init__(
        self,
        id,
        usuario_id,
        token,
        fecha_creacion,
        fecha_expiracion,
        usado,
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.token = token
        self.fecha_creacion = fecha_creacion
        self.fecha_expiracion = fecha_expiracion
        self.usado = usado