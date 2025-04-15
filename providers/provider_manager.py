from providers.exceptions import ProviderException
from providers.translations import TranslationProvider
from providers.transcriptions import TranscriptionProvider

class ProviderManager:

    def __init__(self):
        self.transcription_providers: dict[str, TranscriptionProvider] = {}
        self.translation_providers: dict[str, TranslationProvider] = {}

    def add_transcription_provider(self, provider_name: str,
                                   provider: TranscriptionProvider):
        self.transcription_providers[provider_name] = provider

    def add_translation_provider(self, provider_name: str,
                                 provider: TranslationProvider):
        self.translation_providers[provider_name] = provider

    def get_transcription_provider(self, provider_name: str) -> TranscriptionProvider:
        try: return self.transcription_providers[provider_name]

        except KeyError: raise ProviderException(f"Provider {provider_name} not found")

    def get_translation_provider(self, provider_name: str) -> TranslationProvider:
        try: return self.translation_providers[provider_name]

        except KeyError: raise ProviderException(f"Provider {provider_name} not found")

    async def get_transcription_providers_labels(self) -> dict[str, str]:
        provider_list: dict[str, str] = {}
        for provider in self.transcription_providers.keys():
            provider_list[provider] = await self.transcription_providers[provider].get_label()

        return provider_list
