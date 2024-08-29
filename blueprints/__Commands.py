from telethon import TelegramClient, events
import messages


class __Commands:

    def __init__(self, client: TelegramClient):

        @client.on(events.NewMessage(pattern='/start'))
        async def start(event: events.NewMessage.Event):
            await client.send_message(event.chat_id, messages.start)

        @client.on(events.NewMessage(pattern='/privacy'))
        async def privacy(event: events.NewMessage.Event):
            await client.send_message(event.chat_id, messages.privacy)

        @client.on(events.NewMessage(pattern='/help'))
        async def help(event: events.NewMessage.Event):
            await client.send_message(event.chat_id, messages.help)