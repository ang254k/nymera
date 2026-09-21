import os
import sys
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.repositories.sueno_repository import SuenoRepository

NUM_SUEÑOS = 30

USUARIO_ID = 4

CATEGORIAS = list(range(1, 10))


TITULOS = [
    "Un sueño extraño",
    "La ciudad de cristal",
    "El bosque infinito",
    "Una noche diferente",
    "El tren que no existía",
    "La casa junto al mar",
    "El lugar desconocido",
    "Una puerta misteriosa",
    "Volando sobre la ciudad",
    "El día que todo cambió",
]


CONTENIDOS = [
    "Soñé que caminaba por un lugar que no reconocía y todo parecía completamente real.",
    "Estaba en una ciudad enorme donde los edificios cambiaban de forma cada vez que los miraba.",
    "Me encontraba en un bosque interminable y no conseguía encontrar el camino de vuelta.",
    "Todo comenzó como una noche normal, pero poco a poco las cosas empezaron a volverse extrañas.",
    "Subí a un tren que viajaba hacia un destino que no aparecía en ningún mapa.",
    "Había una casa junto al mar y tenía la sensación de que ya había estado allí muchas veces.",
]


def crear_suenos():
    repository = SuenoRepository()

    for i in range(NUM_SUEÑOS):
        titulo = f"{random.choice(TITULOS)} #{i + 1}"
        contenido = random.choice(CONTENIDOS)
        categoria_id = random.choice(CATEGORIAS)

        sueno = repository.create(
            titulo=titulo,
            contenido=contenido,
            usuario_id=USUARIO_ID,
            categoria_id=categoria_id,
            publico=True,
        )

        print(
            f"Creado sueño {sueno.id}: "
            f"{sueno.titulo} | categoría {categoria_id}"
        )


if __name__ == "__main__":
    crear_suenos()