import base64
import os
import time

import requests
from file_manipulation import DownloadListener


class RunPodConnector:
    def __init__(self, api_key: str, runpod_url: str, download_listener: DownloadListener):
        self.api_key = api_key
        self.runpod_url = runpod_url
        self.download_listener = download_listener


    async def _get_job_status(self, job_id: str) -> object:
        response = requests.get(
            url=self.runpod_url + "/status/" + job_id,
            headers={
                "Authorization": "Bearer " + self.api_key,
                "Content-Type": "application/json"
            })

        return response.json()

    async def transcribe(self, audio_file: str) -> None:
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



        job = requests.post(
            url=self.runpod_url + "/run",
            headers={
                "Authorization": "Bearer " + self.api_key,
                "Content-Type": "application/json"
            },
            json=json
        )

        job_id = job.json()["id"]

        while True:
            job = await self._get_job_status(job_id)
            if job["status"] == "COMPLETED":
                 return job["output"]["transcription"]

            elif job["status"] in ["FAILED", "CANCELLED", "TIMED_OUT"]:
                raise Exception(f"Job failed with status {job['status']}")

            time.sleep(5)
