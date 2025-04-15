import deepl
from . import TranslationProvider

class DeepLTranslator(TranslationProvider):
    def __init__(self, api_key):
        self.api_key = api_key
        self.translator = deepl.Translator(self.api_key)

    async def translate(self, text, target_lang, source_language: str = None) -> str:
        try:
            result = self.translator.translate_text(text, target_lang=target_lang)
            return result.text

        except Exception as e:
            print(e.with_traceback(e.__traceback__))
            return "Language not supported. Use /lang to set a language for translations"
