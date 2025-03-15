from telegram import Update
from telegram.ext import Application, ContextTypes
from telethon import TelegramClient, events

from database import DBConnector
from translation import Translator


class __Translations:

    def __init(self, client: TelegramClient,
               ptb_instance: Application,
               db_connector: DBConnector,
               translator: Translator):

        self.client = client
        self.ptb_instance = ptb_instance
        self.db_connector = db_connector
        self.translator = translator

