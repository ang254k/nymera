from app.repositories.hashtag_repository import HashtagRepository


class HashtagService:

    def __init__(self):
        self.hashtag_repository = HashtagRepository()

    def get_suenos_by_hashtag(
        self, hashtag, usuario_id, categorias=None, ordenar_por=None, direccion=None
    ):

        hashtag_obj = self.hashtag_repository.get_by_nombre(hashtag)

        if hashtag_obj is None:
            raise ValueError("hashtag_not_found")

        return self.hashtag_repository.get_suenos_by_nombre(
            hashtag, usuario_id, categorias, ordenar_por, direccion
        )

    def get_trending(self):
        return self.hashtag_repository.get_trending()
