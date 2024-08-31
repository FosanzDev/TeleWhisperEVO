from telethon import TelegramClient

from genai.RunPodConnector import RunPodConnector
from .__Transcriptions import __Transcriptions
from .__Commands import __Commands
from database import DBConnector
from genai.GenAIConnector import GenAIConnector
from translation import Translator


def register_all(client: TelegramClient,
                 db_connector: DBConnector,
                 genai_connector: GenAIConnector,
                 translator: Translator,
                 runpod_connector: RunPodConnector):
    __Transcriptions(client, genai_connector, runpod_connector)
    __Commands(client)