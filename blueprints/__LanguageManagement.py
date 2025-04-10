from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CallbackQueryHandler, CommandHandler
from telethon import TelegramClient

from database import DBConnector, languages


class __LanguageManagement:
    def __init__(self, client: TelegramClient,
               ptb_instance: Application,
               db_connector: DBConnector):

        self.client = client
        self.ptb_instance = ptb_instance
        self.db_connector = db_connector

        async def change_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
            lang_code: str = db_connector.get_language(update.effective_chat.id)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Select a language for translations",
                                           reply_markup=InlineKeyboardMarkup(await gen_lang_buttons(lang_code)))

        async def callback_langchange(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query
            lang = query.data.split('_')[-1]
            actual = db_connector.get_language(query.from_user.id)
            if lang == actual:
                await query.answer()
                return

            languagename = f"{languages[lang]['label']} {languages[lang]['flag']}"
            db_connector.set_language(query.from_user.id, lang)
            await query.edit_message_text(text=f"Default language set to {languagename}!",
                                          reply_markup=InlineKeyboardMarkup(await gen_lang_buttons(lang)))

        async def __callback_pagechange(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query
            page = int(query.data.split('_')[-1])
            await query.edit_message_text(text="Select a language for translations",
                                          reply_markup=InlineKeyboardMarkup(await gen_lang_buttons(db_connector.get_language(query.from_user.id), page)))



        ptb_instance.add_handler(CommandHandler("lang", change_lang, block=False))
        ptb_instance.add_handler(CallbackQueryHandler(callback_langchange, 'lang_*', block=False))
        ptb_instance.add_handler(CallbackQueryHandler(__callback_pagechange, 'page_lang_*', block=False))


async def gen_lang_buttons(user_lang: str = None, page: int = None, show_selection: bool = True, with_callback: str = 'lang_') -> list:
    # Configuration for button layout
    LANG_BUTTONS_PER_ROW = 2  # Buttons per row
    LANG_BUTTONS_PER_COLUMN = 5  # Rows per page
    LANG_BUTTONS_PER_PAGE = LANG_BUTTONS_PER_ROW * LANG_BUTTONS_PER_COLUMN  # Buttons per page

    if user_lang is None and page is None:
        page = 0

    # Validate and calculate the start page if user_lang is specified
    elif user_lang in languages and page is None:
        page = list(languages.keys()).index(user_lang) // LANG_BUTTONS_PER_PAGE

    # Compute pagination indices
    start_index = page * LANG_BUTTONS_PER_PAGE
    end_index = start_index + LANG_BUTTONS_PER_PAGE + 1
    paginated_langs = list(languages.items())[start_index:end_index]  # Slice based on the page

    # Create buttons for the current page of languages
    lang_buttons = []
    row = []
    for i, (lang_code, lang_data) in enumerate(paginated_langs[1:]):
        label_with_flag = f"{lang_data['label']} {lang_data['flag']}"

        # Highlight the selected language
        if lang_code == user_lang and show_selection:
            button = InlineKeyboardButton(f"✅ {label_with_flag}", callback_data=f"{with_callback}{lang_code}")
        else:
            button = InlineKeyboardButton(label_with_flag, callback_data=f"{with_callback}{lang_code}")

        row.append(button)
        # Add a row when it reaches the configured size
        if len(row) == LANG_BUTTONS_PER_ROW:
            lang_buttons.append(row)
            row = []

    # Add the last row if not empty
    if row:
        lang_buttons.append(row)

    # Add navigation buttons
    nav_buttons = []
    if start_index > 0:  # Add the "Previous" button if there's a preceding page
        nav_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"page_{with_callback}{page - 1}"))
    if end_index < len(languages):  # Add the "Next" button if there's a following page
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"page_{with_callback}{page + 1}"))
    if nav_buttons:
        lang_buttons.append(nav_buttons)  # Append navigation buttons as a new row

    return lang_buttons
