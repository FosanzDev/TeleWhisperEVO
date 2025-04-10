from abc import ABC, abstractmethod

class TranscriptionProvider(ABC):

    @abstractmethod
    async def transcribe(self, audio_file: str) -> str:
        raise NotImplementedError