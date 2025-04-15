from telethon.sync import TelegramClient

from telegram.ext import Application

from providers import ProviderManager
from .__Transcriptions import __Transcriptions
from .__Commands import __Commands
from .__Payments import __Payments
from .__LanguageManagement import __LanguageManagement
from .__Translations import __Translations
from .__ProviderManagement import __ProviderManagement
from database import DBConnector


def register_all(client: TelegramClient,
                 db_connector: DBConnector,
                 provider_manager: ProviderManager,
                 ptb_instance: Application,
                 payment_token: str):
    __Transcriptions(client, ptb_instance, provider_manager, db_connector)
    __Commands(client, db_connector)
    __Payments(ptb_instance, db_connector, payment_token)
    __LanguageManagement(client, ptb_instance, db_connector)
    __ProviderManagement(client, ptb_instance, provider_manager, db_connector)
    __Translations(client, ptb_instance, db_connector, provider_manager)
