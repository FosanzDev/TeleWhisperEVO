import deepl

class Translator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.translator = deepl.Translator(self.api_key)

    def translate(self, text, target_lang) -> str:
        try:
            result = self.translator.translate_text(text, target_lang=target_lang)
            return result.text

        except Exception as e:
            return "Language not supported. Use /lang to set a language for translations"
