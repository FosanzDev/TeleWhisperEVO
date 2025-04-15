from providers.transcriptions import TranscriptionProvider
import requests

class FireworksTranscriber(TranscriptionProvider):

    def __init__(self, api_key: str, service_url: str):
        self.api_key = api_key
        self.service_url = service_url

    async def transcribe(self, audio_file: str) -> str:
        with open(audio_file, "rb") as f:
            response = requests.post(
                url=self.service_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                files={"file": f},
                data={
                    "model": "whisper-v3-turbo",
                    "temperature": "0",
                    "vad_model": "silero"
                },
            )
            return response.json()["text"]

    async def get_label(self) -> str:
        return "whisper-v3-turbo - FireworksAI"