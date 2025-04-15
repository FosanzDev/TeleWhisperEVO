from typing import Any, Coroutine

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler, CallbackQueryHandler
from telethon import TelegramClient

from database import DBConnector, languages
from providers import ProviderManager


class __ProviderManagement:
    def __init__(self, client: TelegramClient,
                 ptb_instance: Application,
                 provider_manager: ProviderManager,
                 db_connector: DBConnector):
        self.client = client
        self.ptb_instance = ptb_instance
        self.db_connector = db_connector
        self.provider_manager = provider_manager

        async def change_transcription_provider(update: Update, context: ContextTypes.DEFAULT_TYPE):
            actual_provider = self.db_connector.get_user_transcription_provider(str(update.effective_chat.id))
            buttons = get_provider_buttons(with_callback='change_trans_provider_',
                                                 selected=actual_provider,
                                                 options=await self.provider_manager.get_transcription_providers_labels())
            # Create an InlineKeyboardMarkup from the buttons list
            reply_markup = InlineKeyboardMarkup(buttons)

            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Select a provider for transcription",
                                           reply_markup=reply_markup)


        async def callback_change_trans_provider(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query
            provider_key = query.data.split('change_trans_provider_')[-1]
            actual_provider = self.db_connector.get_user_transcription_provider(str(query.from_user.id))
            if provider_key == actual_provider:
                await query.answer()
                return

            provider_name = await provider_manager.get_transcription_provider(provider_key).get_label()
            db_connector.set_user_transcription_provider(str(query.from_user.id), provider_key)
            await query.edit_message_text(text=f"Default provider set to {provider_name}!",
                                          reply_markup=InlineKeyboardMarkup(get_provider_buttons(with_callback='change_trans_provider_',
                                                                                                       selected=provider_key,
                                                                                                       options=await self.provider_manager.get_transcription_providers_labels())))

        ptb_instance.add_handler(CommandHandler("transcriber", change_transcription_provider, block=False))
        ptb_instance.add_handler(CallbackQueryHandler(callback_change_trans_provider, 'change_trans_provider_*', block=False))


def get_provider_buttons(with_callback: str,
                               selected: str = None,
                               page: int = None,
                               options: dict = None,
                               show_selection: bool = True) -> list:
    BUTTONS_PER_ROW = 2
    BUTTONS_PER_COLUMN = 5
    BUTTONS_PER_PAGE = BUTTONS_PER_ROW * BUTTONS_PER_COLUMN

    if selected is None and page is None:
        page = 0

    elif selected in options.keys() and page is None:
        page = list(options.keys()).index(selected) // BUTTONS_PER_PAGE

    start_index = page * BUTTONS_PER_PAGE
    end_index = start_index + BUTTONS_PER_PAGE + 1
    paginated_options = list(options.items())[start_index:end_index]

    buttons = []
    row_buttons = []
    for i, (option_key, option_data) in enumerate(paginated_options):

        if option_key == selected and show_selection:
            button = InlineKeyboardButton(f"✅ {option_data}", callback_data=f"{with_callback}{option_key}")
        else:
            button = InlineKeyboardButton(option_data, callback_data=f"{with_callback}{option_key}")

        row_buttons.append(button)
        if len(row_buttons) == BUTTONS_PER_ROW:
            buttons.append(row_buttons)
            row_buttons = []

    if row_buttons:
        buttons.append(row_buttons)

        # Add navigation buttons
    nav_buttons = []
    if start_index > 0:  # Add the "Previous" button if there's a preceding page
        nav_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"page_{with_callback}{page - 1}"))
    if end_index < len(options) and len(options) > BUTTONS_PER_PAGE:  # Add the "Next" button if there's a following page
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"page_{with_callback}{page + 1}"))
    if nav_buttons:
        buttons.append(nav_buttons)  # Append navigation buttons as a new row

    print(f"Buttons: {buttons}")
    return buttons
