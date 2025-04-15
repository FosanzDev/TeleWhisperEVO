import base64
import os
import aiohttp
import asyncio

from file_manipulation import DownloadListener
from . import TranscriptionProvider


class RunPodTranscriber(TranscriptionProvider):
    def __init__(self, api_key: str, runpod_url: str, download_listener: DownloadListener):
        self.api_key = api_key
        self.runpod_url = runpod_url
        self.download_listener = download_listener

    async def _get_job_status(self, job_id: str) -> object:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.runpod_url + "/status/" + job_id,
                headers={
                    "Authorization": "Bearer " + self.api_key,
                    "Content-Type": "application/json"
                }) as response:
                return await response.json()

    async def transcribe(self, audio_file: str) -> str:
        with_link = False

        # Check if audio_file is greater than 7MB
        if os.path.getsize(audio_file) > 7 * 1024 * 1024:
            file = self.download_listener.generate_download_link(audio_file)
            with_link = True
        else:
            file = base64.b64encode(open(audio_file, "rb").read()).decode("utf-8")

        json = {
            "input": {
                "model": "large-v3"
            }
        }

        if with_link:
            json["input"]["audio"] = file
        else:
            json["input"]["audio_base64"] = file

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=self.runpod_url + "/run",
                headers={
                    "Authorization": "Bearer " + self.api_key,
                    "Content-Type": "application/json"
                },
                json=json
            ) as job_response:
                job = await job_response.json()
                job_id = job["id"]

                while True:
                    job_status = await self._get_job_status(job_id)
                    if job_status["status"] == "COMPLETED":
                        return job_status["output"]["transcription"]
                    elif job_status["status"] in ["FAILED", "CANCELLED", "TIMED_OUT"]:
                        raise Exception(f"Job failed with status {job_status['status']}")
                    await asyncio.sleep(5)

    async def get_label(self) -> str:
        return "large-v3 - RunPod Serverless"