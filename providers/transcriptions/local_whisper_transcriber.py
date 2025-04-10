import whisper

from providers.transcriptions import TranscriptionProvider

class LocalWhisperTranscriber(TranscriptionProvider):
    def __init__(self, model_size: str):
        self.model = whisper.load_model(model_size)

    async def transcribe(self, audio_file: str) -> str:
        result = whisper.transcribe(self.model, audio_file)
        return result["text"]