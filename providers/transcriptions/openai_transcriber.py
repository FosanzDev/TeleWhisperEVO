from typing import BinaryIO

from openai import AsyncOpenAI

from . import TranscriptionProvider


class OpenAITranscriber(TranscriptionProvider):

    def __init__(self, api_key, debug=False):
        self.debug = debug
        self.api_key = api_key
        self.client = AsyncOpenAI(api_key=api_key)

    async def transcribe(self, audio_file: str) -> str:
        raise NotImplementedError
