from telethon import TelegramClient, events
import messages
from database import DBConnector


class __Commands:

    def __init__(self, client: TelegramClient,
                 db_connector: DBConnector):

        @client.on(events.NewMessage(pattern='/start'))
        async def start(event: events.NewMessage.Event):
            user = await client.get_entity(event.sender_id)
            await db_connector.register(
                user_id = user.id,
                user_name = user.username
            )
            await client.send_message(event.chat_id, messages.start)

        @client.on(events.NewMessage(pattern='/privacy'))
        async def privacy(event: events.NewMessage.Event):
            await client.send_message(event.chat_id, messages.privacy)

        @client.on(events.NewMessage(pattern='/help'))
        async def help(event: events.NewMessage.Event):
            await client.send_message(event.chat_id, messages.help)