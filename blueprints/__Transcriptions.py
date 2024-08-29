from telethon import events, TelegramClient

import telethon.utils
import file_manipulation

from genai.GenAIConnector import GenAIConnector


class __Transcriptions:
    def __init__(self, client: TelegramClient,
                 genai_connector: GenAIConnector):

        @client.on(events.NewMessage())
        async def transcribe(event: events.NewMessage.Event):
            if event.message.media:
                if telethon.utils.is_audio(event.message.media):
                    file_path = await event.download_media(file='audio/')
                    mp3_filepath, file_stream = await file_manipulation.auto_to_mp3(file_path)
                    await file_manipulation.remove_file(file_path)
                    text = await genai_connector.transcribe_audio(pro_mode=True, file_path=file_stream)
                    await event.reply(text)
                    await file_manipulation.remove_file(mp3_filepath)
