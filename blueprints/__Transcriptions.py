from uuid import uuid4

from telethon.sync import TelegramClient, events

import telethon.utils
import file_manipulation
from blueprints.utils import get_file_name
from database import DBConnector

from genai.RunPodConnector import RunPodConnector


class __Transcriptions:
    def __init__(self, client: TelegramClient,
                 runpod_connector: RunPodConnector,
                 db_connector: DBConnector):

        self.client = client
        self.runpod_connector = runpod_connector
        self.db_connector = db_connector

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
                                                  file_path=file_path,
                                                  group=True)

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
                                              file_path=file_path,
                                              group=False)

                    else:
                        await event.reply('Reply and click -> /tw_transcribe to transcribe it!')

    async def transcribe(self, event: events.NewMessage.Event,
                         media_message,
                         status_message,
                         group: bool,
                         file_path: str):

        await self.client.edit_message(status_message, parse_mode='html',
                                      message='<i>Converting...</i>')
        try:
            mp3_filepath, file_stream = await file_manipulation.auto_to_mp3(file_path)

        except Exception as e:
            error_id = uuid4()
            await self.db_connector.register_error(
                error_id=error_id,
                user_id=event.message.sender_id,
                action='conversion',
                error=str(e)
            )
            await self.client.edit_message(status_message, parse_mode='Markdown',
                                          message=f'There has been conversion error!\n'
                                                  f'Explain cause at @TeleWhisperSupport.\n'
                                                  f'Error ID: `{error_id}`')
            await file_manipulation.remove_file(file_path)
            return

        #Get duration of the audio file
        duration = await file_manipulation.get_duration(mp3_filepath)
        if duration == -1:
            error_id = uuid4()
            await self.db_connector.register_error(
                error_id=error_id,
                user_id=event.message.sender_id,
                action='duration',
                error='Error getting duration'
            )
            await self.client.edit_message(status_message, parse_mode='Markdown',
                                            message=f'There has been an analysis error!\n'
                                                    f'Explain cause at @TeleWhisperSupport.\n'
                                                    f'Error ID: `{error_id}`')

            await file_manipulation.remove_file(mp3_filepath, file_path)
            return

        # Check if the user has enough credits
        if await self.db_connector.get_credits(event.message.sender_id) < duration:
            if group:
                await self.client.send_message(event.message.chat_id, parse_mode='html',
                                            message='<b>Not enough credits!</b>. Add more in @tw_evo_bot')
            else:
                await self.client.edit_message(status_message, parse_mode='html',
                                           message='<b>Not enough credits!</b>. Add more by clicking -> /top_balance!')
            await file_manipulation.remove_file(mp3_filepath, file_path)
            return

        # Remove the original file
        if file_path != mp3_filepath:
            await file_manipulation.remove_file(file_path)

        # Transcribe the audio file
        await self.client.edit_message(status_message, parse_mode='html',
                                    message='<i>Transcribing...</i>')
        try:
            text = await self.runpod_connector.transcribe(mp3_filepath)
        except Exception as e:
            error_id = uuid4()
            await self.db_connector.register_error(
                error_id=error_id,
                user_id=event.message.sender_id,
                action='transcription',
                error=str(e)
            )
            await self.client.edit_message(status_message, parse_mode='Markdown',
                                          message=f'There has been an error!\n'
                                                  f'Explain cause at @TeleWhisperSupport.\n'
                                                  f'Error ID: `{error_id}`')

            await file_manipulation.remove_file(mp3_filepath)
            return

        # Send the transcription in chunks
        await self.client.send_message(reply_to=media_message.id,
                                       entity=media_message.chat_id,
                                       message=text[:4095])

        for i in range(4095, len(text), 4095):
            await self.client.send_message(event.message.chat_id, text[i:i+4095])

        if len(text) > 4095:
            await self.client.send_message(event.message.chat_id, "All-in-one transcription here!")
            filepath = await file_manipulation.write_to_file(text, mp3_filepath.replace('.mp3', '.html'))
            await self.client.send_file(event.message.chat_id, filepath, reply_to=media_message.id)

        await self.client.edit_message(status_message, parse_mode='html',
                                      message='<b>Done!</b>')
        await file_manipulation.remove_file(mp3_filepath)

        # Deduct credits
        await self.db_connector.register_action(
            user_id=event.message.sender_id,
            action='transcription',
            length=duration,
            cost=duration
        )

        await self.client.delete_messages(event.message.chat_id, [status_message.id])