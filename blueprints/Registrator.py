from telethon import TelegramClient

from .__Transcriptions import __Transcriptions
from .__Commands import __Commands
from database import DBConnector
from genai.GenAIConnector import GenAIConnector
from translation import Translator


def register_all(client: TelegramClient,
                 db_connector: DBConnector,
                 genai_connector: GenAIConnector,
                 translator: Translator):
    __Transcriptions(client, genai_connector)
    __Commands(client)