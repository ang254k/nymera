class Categoria:
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }

    def __repr__(self):
        return f"Categoria(id={self.id}, nombre='{self.nombre}')"
