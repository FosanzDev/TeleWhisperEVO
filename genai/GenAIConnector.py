from typing import BinaryIO

from openai import AsyncOpenAI


class GenAIConnector:

    def __init__(self, api_key, debug=False):
        self.debug = debug
        self.api_key = api_key
        self.client = AsyncOpenAI(api_key=api_key)

    async def transcribe_audio(self, pro_mode: bool = False, file: str | BinaryIO = None):
        if self.debug:
            if pro_mode:
                result = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=file,
                )
                return result.text
            else:
                return 'This is a transcription of an audio file.'
