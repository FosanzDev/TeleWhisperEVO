import asyncio
import copy
from concurrent.futures.thread import ThreadPoolExecutor

import whisper

from providers.transcriptions import TranscriptionProvider

class LocalWhisperTranscriber(TranscriptionProvider):
    def __init__(self, model_size: str):
        self.model_size = model_size
        self.model = whisper.load_model(model_size)
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def transcribe(self, audio_file: str) -> str:
        loop = asyncio.get_event_loop()
        model_copy = copy.deepcopy(self.model)
        transcript = await loop.run_in_executor(self.executor, whisper.transcribe, model_copy, audio_file)
        del model_copy
        return transcript["text"]

    async def get_label(self) -> str:
        return  self.model_size + " - Local Whisper"