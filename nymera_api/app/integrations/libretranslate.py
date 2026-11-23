import requests
from app.config import settings


class TranslationServiceError(Exception):
    def __init__(self, error_key: str, status_code: int = 502):
        self.error_key = error_key
        self.status_code = status_code
        super().__init__(error_key)


class LibreTranslateIntegration:

    def translate(self, texto, idioma_origen, idioma_destino):
        try:
            response = requests.post(
                f"{settings.LIBRETRANSLATE_URL}/translate",
                json={
                    "q": texto,
                    "source": idioma_origen,
                    "target": idioma_destino,
                    "format": "text",
                },
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data["translatedText"]

        except requests.exceptions.Timeout:
            raise TranslationServiceError("translation_timeout", status_code=504)

        except requests.exceptions.HTTPError as exc:
            status_code = exc.response.status_code if exc.response is not None else 502
            if status_code == 429:
                raise TranslationServiceError("translation_rate_limit", status_code=429)
            raise TranslationServiceError("translation_unavailable", status_code=502)

        except (requests.exceptions.RequestException, KeyError):
            raise TranslationServiceError("translation_unavailable", status_code=502)