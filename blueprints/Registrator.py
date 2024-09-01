from telethon import TelegramClient

from telegram.ext import Application

from genai.RunPodConnector import RunPodConnector
from .__Transcriptions import __Transcriptions
from .__Commands import __Commands
from .__Payments import __Payments
from database import DBConnector
from genai.GenAIConnector import GenAIConnector
from translation import Translator


def register_all(client: TelegramClient,
                 db_connector: DBConnector,
                 genai_connector: GenAIConnector,
                 translator: Translator,
                 runpod_connector: RunPodConnector,
                 ptb_instance: Application):
    __Transcriptions(client, runpod_connector)
    __Commands(client, db_connector)
    __Payments(ptb_instance)