import configparser
from telethon import TelegramClient, events
from telethon.events.common import EventBuilder, EventCommon

from database.DBConnector import DBConnector
from genai.GenAIConnector import GenAIConnector
from translation.Translator import Translator

config = configparser.ConfigParser()
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

genai_connector = GenAIConnector(api_key=config['OpenAI']['api_key'])
translator = Translator(api_key=config['DeepL']['api_key'])


@client.on(events.NewMessage())
async def my_event_handler(event):
    if event.is_private:
        await event.reply('This is a private chat.')



if __name__ == '__main__':
    client.run_until_disconnected()
