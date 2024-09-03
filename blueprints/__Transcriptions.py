from uuid import uuid4

from telethon.sync import TelegramClient, events

import telethon.utils
import file_manipulation
from blueprints.utils import get_file_name

from genai.RunPodConnector import RunPodConnector


class __Transcriptions:
    def __init__(self, client: TelegramClient,
                 runpod_connector: RunPodConnector):

        self.client = client
        self.runpod_connector = runpod_connector

        @client.on(events.NewMessage(pattern='/tw_transcribe'))
        async def group_transcribe(event: events.NewMessage.Event):
            if event.is_private:
                await event.reply('Send me an audio file to transcribe!')
            else:
                # Get the replying message:
                reply_message = await event.get_reply_message()
                if reply_message is None:
                    await event.reply('Reply and click -> /tw_transcribe to transcribe anything!')
                else:
                    if reply_message.media:
                        if telethon.utils.is_audio(reply_message.media):
                            status_message = await client.send_message(event.chat_id, parse_mode='html',
                                                                  message='<em>Receiving file...</em>')
                            file_name = str(uuid4()) + '.' + get_file_name(reply_message).split('.')[-1]
                            file_path = await reply_message.download_media(file='audio/' + file_name)

                            await self.transcribe(event=event,
                                                  media_message=reply_message,
                                                  status_message=status_message,
                                                  file_path=file_path)

                    else:
                        await event.reply("I can't transcribe that!")


        @client.on(events.NewMessage())
        async def private_transcribe(event: events.NewMessage.Event):
            if event.message.media:
                if telethon.utils.is_audio(event.message.media):
                    if event.is_private:
                        status_message = await client.send_message(event.chat_id, parse_mode='html',
                                                                    message='<em>Receiving file...</em>')

                        file_name = str(uuid4()) + '.' + get_file_name(event.message).split('.')[-1]
                        file_path = await event.download_media(file='audio/' + file_name)
                        await self.transcribe(event=event,
                                              media_message=event.message,
                                              status_message=status_message,
                                              file_path=file_path)

                    else:
                        await event.reply('Reply and click -> /tw_transcribe to transcribe it!')

    async def transcribe(self, event: events.NewMessage.Event,
                         media_message,
                         status_message,
                         file_path: str):

        await self.client.edit_message(status_message, parse_mode='html',
                                      message='<i>Converting...</i>')
        mp3_filepath, file_stream = await file_manipulation.auto_to_mp3(file_path)
        if file_path != mp3_filepath:
            await file_manipulation.remove_file(file_path)

        await self.client.edit_message(status_message, parse_mode='html',
                                    message='<i>Transcribing...</i>')
        text = await self.runpod_connector.transcribe(mp3_filepath)
        await self.client.send_message(reply_to=media_message.id,
                                       entity=media_message.chat_id,
                                       message=text[:4095])
        for i in range(4095, len(text), 4095):
            await self.client.send_message(event.message.chat_id, text[i:i+4095])

        await self.client.edit_message(status_message, parse_mode='html',
                                      message='<b>Done!</b>')
        await file_manipulation.remove_file(mp3_filepath)

        await self.client.delete_messages(event.message.chat_id, [status_message.id])