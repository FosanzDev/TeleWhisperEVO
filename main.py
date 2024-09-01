import configparser

from telethon import TelegramClient

from telegram.ext import ApplicationBuilder

from blueprints import register_all
from file_manipulation import DownloadListener
from genai.RunPodConnector import RunPodConnector

# DEBUG MODE CONTROL
DEBUG = False

from database.DBConnector import DBConnector
from genai.GenAIConnector import GenAIConnector
from translation.Translator import Translator

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

genai_connector = GenAIConnector(api_key=config['OpenAI']['api_key'], debug=DEBUG)
translator = Translator(api_key=config['DeepL']['api_key'])

download_listener = DownloadListener(host_ip=config['Downloads']['host'],
                                     port=int(config['Downloads']['port']))

runpod_connector = RunPodConnector(api_key=config['RunPod']['api_key'],
                                   runpod_url=config['RunPod']['url'],
                                   download_listener=download_listener)

ptb_instance = ApplicationBuilder().token(config['Telegram']['bot_token']).build()

register_all(client=client,
             db_connector= dbConnector,
             genai_connector= genai_connector,
             translator= translator,
             runpod_connector= runpod_connector,
             ptb_instance= ptb_instance)

if __name__ == '__main__':
    download_listener.run_in_thread()
    ptb_instance.run_polling(poll_interval=2)
    client.run_until_disconnected()
