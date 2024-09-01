from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application, MessageHandler, filters


class __Payments:
    def __init__(self, ptb_instance: Application):

        async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo, block=False)

        ptb_instance.add_handler(echo_handler)