class Like:
    def __init__(self, usuario_id, sueno_id, fecha):
        self.usuario_id = usuario_id
        self.sueno_id = sueno_id
        self.fecha = fecha
    def __repr__(self):
        return (
            f"Like(usuario_id={self.usuario_id}, "
            f"sueno_id={self.sueno_id})"
        )