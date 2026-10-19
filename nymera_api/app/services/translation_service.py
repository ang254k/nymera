from app.integrations.libretranslate import LibreTranslateIntegration

class TranslationService:

    def __init__(self):
        self.translator = LibreTranslateIntegration()
        
    def translate(self, texto, idioma_origen, idioma_destino):
        return self.translator.translate(
            texto,
            idioma_origen,
            idioma_destino
        )