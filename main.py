import configparser
from telethon import TelegramClient, events
from telethon.events.common import EventBuilder

config = configparser.ConfigParser()
config.read('env.ini')

api_id = int(config['Telegram']['api_id'])
api_hash = config['Telegram']['api_hash']

client = (TelegramClient('TeleWhisperEVO', api_id=api_id, api_hash=api_hash)
          .start(bot_token=config['Telegram']['bot_token']))


@client.on(EventBuilder.build(events.NewMessage))
async def my_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi!')


if __name__ == '__main__':
    client.run_until_disconnected()
