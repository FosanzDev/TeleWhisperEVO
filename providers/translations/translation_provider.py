from abc import ABC, abstractmethod

class TranslationProvider(ABC):

    @abstractmethod
    async def translate(self, text: str, target_language: str, source_language: str = None) -> str:
        raise NotImplementedError