from uuid import uuid4

from telethon import events, TelegramClient

import telethon.utils
import file_manipulation
from blueprints.utils import get_file_name

from genai.RunPodConnector import RunPodConnector


class __Transcriptions:
    def __init__(self, client: TelegramClient,
                 runpod_connector: RunPodConnector):

        @client.on(events.NewMessage())
        async def transcribe(event: events.NewMessage.Event):
            if event.message.media:
                if telethon.utils.is_audio(event.message.media):
                    status_message = await client.send_message(event.message.chat_id, parse_mode='html',
                                                            message='<em>Receiving file...</em>')
                    file_name = str(uuid4()) + '.' + get_file_name(event.message).split('.')[-1]
                    file_path = await event.download_media(file='audio/' + file_name)

                    await client.edit_message(status_message, parse_mode='html',
                                              message='<i>Converting...</i>')
                    mp3_filepath, file_stream = await file_manipulation.auto_to_mp3(file_path)
                    if file_path != mp3_filepath: # If the file was not an mp3, remove the original file
                        await file_manipulation.remove_file(file_path)

                    await client.edit_message(status_message, parse_mode='html',
                                              message='<i>Transcribing...</i>')
                    text = await runpod_connector.transcribe(mp3_filepath)
                    await event.reply(text)
                    await client.edit_message(status_message, parse_mode='html',
                                              message='<b>Done!</b>')
                    await file_manipulation.remove_file(mp3_filepath)
                    await client.delete_messages(event.message.chat_id, [status_message.id])
