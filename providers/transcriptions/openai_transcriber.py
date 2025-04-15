from openai import AsyncOpenAI

from . import TranscriptionProvider


class OpenAITranscriber(TranscriptionProvider):

    def __init__(self, api_key):
        self.api_key = api_key
        self.client = AsyncOpenAI(api_key=api_key)

    async def transcribe(self, audio_file: str) -> str:
        return await self.client.audio.transcriptions.create(
            model="whisper-1",
            file=open(audio_file, "rb"),
            response_format="text"
        )

    async def get_label(self) -> str:
        return "whisper-1 - OpenAI API"