from uuid import uuid4

from telegram.ext import Application
from telethon.sync import TelegramClient, events

import telethon.utils
import file_manipulation
from blueprints.__Translations import assign_translation_possibility
from blueprints.utils import get_file_name
from database import DBConnector

from providers import ProviderManager
from providers.transcriptions import TranscriptionProvider
from providers.exceptions import ProviderException


class __Transcriptions:
    def __init__(self, client: TelegramClient,
                 ptb_instance: Application,
                 provider_manager: ProviderManager,
                 db_connector: DBConnector):

        self.client = client
        self.ptb_instance = ptb_instance
        self.provider_manager = provider_manager
        self.db_connector = db_connector
        self.contexts = {}

        @client.on(events.NewMessage(pattern='/tw_transcribe'))
        async def group_transcribe(event: events.NewMessage.Event):
            if event.is_private:
                await event.reply('Send me any multimedia file to transcribe!')
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
                                                  #TODO: Add more providers
                                                  provider_key='runpod',
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
                                              #TODO: Add more provider keys
                                              provider_key='runpod',
                                              file_path=file_path,
                                              group=False)

                    else:
                        await event.reply('Reply and click -> /tw_transcribe to transcribe it!')

    async def transcribe(self, event: events.NewMessage.Event,
                         media_message,
                         status_message,
                         provider_key: str,
                         group: bool,
                         file_path: str):

        try:
            provider: TranscriptionProvider = self.provider_manager.get_transcription_provider(provider_key)
        except ProviderException:
            await self.raise_error(status_message, event.message.sender_id, 'provider', 'Invalid provider key')
            return

        await self.client.edit_message(status_message, parse_mode='html',
                                      message='<i>Converting...</i>')
        try:
            mp3_filepath, file_stream = await file_manipulation.auto_to_mp3(file_path)

        except Exception as e:
            await self.raise_error(status_message, event.message.sender_id, 'conversion', str(e))
            await file_manipulation.remove_file(file_path)
            return

        #Get duration of the audio file
        duration = await file_manipulation.get_duration(mp3_filepath)
        if duration == -1:
            await self.raise_error(status_message, event.message.sender_id, 'duration', 'Error getting duration')
            await file_manipulation.remove_file(mp3_filepath, file_path)
            return

        is_privileged = self.db_connector.is_privileged(event.message.sender_id)

        # Changed behavior to allow transcription of files up to 15 minutes
        # If the file is longer than 15 minutes, only privileged users can transcribe it
        if duration > 900 and not is_privileged:
        # if self.db_connector.get_credits(event.message.sender_id) < duration:
            if group:
                await self.client.send_message(event.message.chat_id, parse_mode='html',
                                            message='<b>Not a SuperUser!</b>. To transcribe more than 15 minutes, contact @Fosanz')
            else:
                await self.client.edit_message(status_message, parse_mode='html',
                                           message='<b>Not a SuperUser!</b>. To transcribe more than 15 minutes, contact @Fosanz')
            await file_manipulation.remove_file(mp3_filepath, file_path)
            return

        # Remove the original file
        if file_path != mp3_filepath:
            await file_manipulation.remove_file(file_path)

        # Transcribe the audio file
        await self.client.edit_message(status_message, parse_mode='html',
                                    message='<i>Transcribing. Cold instance starts might take up to 30 seconds...</i>')
        try:
            text = await provider.transcribe(mp3_filepath)
        except Exception as e:
            await self.raise_error(status_message, event.message.sender_id, 'transcription', str(e))
            await file_manipulation.remove_file(mp3_filepath)
            return

        # Send the transcription in chunks
        txt_message = await self.client.send_message(reply_to=media_message.id,
                                       entity=media_message.chat_id,
                                       message=text[:4095])

        for i in range(4095, len(text), 4095):
            await self.client.send_message(event.message.chat_id, text[i:i+4095])

        if len(text) > 4095:
            filepath = await file_manipulation.write_to_file(text, mp3_filepath.replace('.mp3', '.txt'))
            txt_message = await self.client.send_file(event.message.chat_id,
                                        filepath,
                                        reply_to=media_message.id,
                                        caption="Big transcription!, here's a txt file with the full transcription ;D")

            await file_manipulation.remove_file(filepath)

        lang = self.db_connector.get_language(event.message.sender_id)
        await assign_translation_possibility(self, lang, event.chat_id, txt_message.id)

        await self.client.edit_message(status_message, parse_mode='html',
                                      message='<b>Done!</b>')

        await self.client.send_message(event.message.chat_id, parse_mode='html',
                                       message="Hey! The bot is <i>free</i>, but increased usage is not rentable for the developer.<br>"
                                               "Consider donating to keep the service running!")
        await file_manipulation.remove_file(mp3_filepath)

        # Deduct credits
        self.db_connector.register_action(
            user_id=event.message.sender_id,
            action='transcription',
            length=duration,
            cost=duration
        )

        await self.client.delete_messages(event.message.chat_id, [status_message.id])

    async def raise_error(self, status_message, user_id, action, error):
        error_id = uuid4()
        self.db_connector.register_error(
            error_id=error_id,
            user_id=user_id,
            action=action,
            error=error
        )
        await self.client.edit_message(status_message, parse_mode='Markdown',
                                    message=f'There has been an error!\n'
                                            f'Explain cause at @TeleWhisperSupport.\n'
                                            f'Error ID: `{error_id}`')
        return