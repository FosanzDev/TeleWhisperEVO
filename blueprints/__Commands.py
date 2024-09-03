from telethon.sync import TelegramClient, events
import messages
from database import DBConnector


class __Commands:

    def __init__(self, client: TelegramClient,
                 db_connector: DBConnector):

        # ----------- PRIVATE COMMANDS ------------

        @client.on(events.NewMessage(pattern='/start'))
        async def start(event: events.NewMessage.Event):
            if event.is_private:
                user = await client.get_entity(event.sender_id)
                await db_connector.register(
                    user_id = user.id,
                    user_name = user.username
                )
                await client.send_message(event.chat_id, messages.start)

        @client.on(events.NewMessage(pattern='/privacy'))
        async def privacy(event: events.NewMessage.Event):
            if event.is_private:
                await client.send_message(event.chat_id, messages.privacy)

        @client.on(events.NewMessage(pattern='/help'))
        async def help(event: events.NewMessage.Event):
            if event.is_private:
                await client.send_message(event.chat_id, messages.help)

        @client.on(events.NewMessage(pattern='/intro'))
        async def intro(event: events.NewMessage.Event):
            if event.is_private:
                await client.send_message(event.chat_id, messages.intro)

        @client.on(events.NewMessage(pattern='/coming_soon'))
        async def coming_soon(event: events.NewMessage.Event):
            if event.is_private:
                await client.send_message(event.chat_id, messages.coming_soon)

        @client.on(events.NewMessage(pattern='/credits'))
        async def credits(event: events.NewMessage.Event):
            if event.is_private:
                user_credits = await db_connector.get_credits(event.sender_id)
                if user_credits is None:
                    await client.send_message(event.chat_id, messages.not_registered)
                await client.send_message(event.chat_id, messages.credits.format(user_credits))

        # ----------- GROUP COMMANDS ------------

        @client.on(events.NewMessage(pattern='/tw_privacy'))
        async def tw_privacy(event: events.NewMessage.Event):
            if not event.is_private:
                await event.reply(messages.privacy)

        @client.on(events.NewMessage(pattern='/tw_help'))
        async def tw_help(event: events.NewMessage.Event):
            if not event.is_private:
                await event.reply(messages.group_help)

        @client.on(events.NewMessage(pattern='/tw_credits'))
        async def tw_credits(event: events.NewMessage.Event):
            if not event.is_private:
                user_credits = await db_connector.get_credits(event.sender_id)
                if user_credits is None:
                    await client.send_message(event.chat_id, messages.not_registered)
                await event.reply(messages.credits.format(user_credits))