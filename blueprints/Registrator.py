from telethon.sync import TelegramClient

from telegram.ext import Application

from genai.RunPodConnector import RunPodConnector
from .__Transcriptions import __Transcriptions
from .__Commands import __Commands
from .__Payments import __Payments
from .__LanguageManagement import __LanguageManagement
from .__Translations import __Translations
from database import DBConnector
from genai.GenAIConnector import GenAIConnector
from translation import Translator


def register_all(client: TelegramClient,
                 db_connector: DBConnector,
                 genai_connector: GenAIConnector,
                 translator: Translator,
                 runpod_connector: RunPodConnector,
                 ptb_instance: Application,
                 payment_token: str):
    __Transcriptions(client, ptb_instance, runpod_connector, db_connector)
    __Commands(client, db_connector)
    __Payments(ptb_instance, db_connector, payment_token)
    __LanguageManagement(client, ptb_instance, db_connector)
    __Translations(client, ptb_instance, db_connector, translator)
