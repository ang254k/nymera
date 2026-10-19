import requests
from app.config import settings

class LibreTranslateIntegration:

    def translate(self, texto, idioma_origen, idioma_destino):
        response = requests.post(
            f"{settings.LIBRETRANSLATE_URL}/translate",
            json={
                "q": texto,
                "source": idioma_origen,
                "target": idioma_destino,
                "format": "text",
            },
            timeout=10,
        )
        
        response.raise_for_status()
        
        data = response.json()
        
        return data["translatedText"]