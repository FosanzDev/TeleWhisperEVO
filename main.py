import asyncio
import configparser

from telethon.sync import TelegramClient

from telegram.ext import ApplicationBuilder

from blueprints import register_all
from file_manipulation import DownloadListener
from providers import ProviderManager
from providers.transcriptions.fireworks_transcriber import FireworksTranscriber
from providers.transcriptions.local_whisper_transcriber import LocalWhisperTranscriber
from providers.transcriptions.runpod_transcriber import RunPodTranscriber

# DEBUG MODE CONTROL
DEBUG = False

from database.DBConnector import DBConnector
from providers.transcriptions.openai_transcriber import OpenAITranscriber
from providers.translations.deepl_translator import DeepLTranslator

config = configparser.ConfigParser()
if DEBUG:
    config.read('env.debug.ini')
else:
    config.read('env.ini')

api_id = int(config['Telegram']['api_id'])
api_hash = config['Telegram']['api_hash']

client = (TelegramClient('TeleWhisperEVO', api_id=api_id, api_hash=api_hash)
          .start(bot_token=config['Telegram']['bot_token']))

dbConnector = DBConnector(
    host=config['Database']['host'],
    port=config['Database']['port'],
    database=config['Database']['database'],
    username=config['Database']['username'],
    password=config['Database']['password']
)
download_listener = DownloadListener(host_ip=config['Downloads']['host'],
                                     port=int(config['Downloads']['port']))


provider_manager = ProviderManager()
provider_manager.add_transcription_provider(
    'openai',
    OpenAITranscriber(api_key=config['OpenAI']['api_key'])
)

provider_manager.add_transcription_provider(
    'runpod',
    RunPodTranscriber(api_key=config['RunPod']['api_key'],
                      runpod_url=config['RunPod']['url'],
                      download_listener=download_listener)
)

provider_manager.add_transcription_provider(
    'fireworks',
    FireworksTranscriber(api_key=config['FireworksAI']['api_key'],
                         service_url=config['FireworksAI']['url'])
)

provider_manager.add_translation_provider(
    'deepl',
    DeepLTranslator(api_key=config['DeepL']['api_key'])
)

if config['Local']['use_local_whisper'] == 'True':
    provider_manager.add_transcription_provider(
        'local_whisper',
        LocalWhisperTranscriber(config['Local']['model_size'])
    )

payment_token = config['Payments']['default_token']
ptb_instance = ApplicationBuilder().token(config['Telegram']['bot_token']).build()

register_all(client=client,
             db_connector= dbConnector,
             provider_manager= provider_manager,
             ptb_instance= ptb_instance,
             payment_token= payment_token)

if __name__ == '__main__':
    download_listener.run_in_thread()
    ptb_instance.run_polling(poll_interval=2)
    asyncio.get_event_loop().run_until_complete(client.run_until_disconnected())
