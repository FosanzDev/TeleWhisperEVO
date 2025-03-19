from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton, Message
from telegram.ext import Application, ContextTypes, CallbackContext, CallbackQueryHandler
from telethon import TelegramClient

import file_manipulation
from blueprints.__LanguageManagement import gen_lang_buttons
from database import DBConnector, languages
from translation import Translator


class __Translations:

    def __init__(self, client: TelegramClient,
               ptb_instance: Application,
               db_connector: DBConnector,
               translator: Translator):

        self.client = client
        self.ptb_instance = ptb_instance
        self.db_connector = db_connector
        self.translator = translator

        async def __callback_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query # No possibility for the message to be MaybeInaccessibleMessage
            lang = query.data.split('_')[-1]
            translation: str
            if query.message.document:
                txt = await context.bot.get_file(query.message.document.file_id)
                await txt.download_to_drive(f'audio/{query.message.document.file_name}')
                with open(f'audio/{query.message.document.file_name}', 'r+') as f:
                    text = f.read()

                    status = await context.bot.send_message(chat_id=query.from_user.id, text="Translating...")

                    translation = await translator.translate(text, lang)

                    for i in range(0, len(translation), 4095):
                        await context.bot.send_message(chat_id=query.from_user.id, text=translation[i:i + 4095])

                    await status.delete()

                    f.seek(0)
                    f.write(translation)
                    f.truncate()
                    
                    f.seek(0)
                    await context.bot.send_document(
                        chat_id=query.from_user.id,
                        document=f,
                        caption=f"Translated to {languages[lang]['label']}"
                    )

                await file_manipulation.remove_file(f'audio/{query.message.document.file_name}')

            elif query.message.text:
                text = query.message.text
                status = await context.bot.send_message(
                    chat_id=query.from_user.id,
                    text=f"Translating..."
                )
                translation = await translator.translate(text, lang)
                await context.bot.edit_message_text(
                    chat_id=query.from_user.id, 
                    message_id=status.id,
                    text=f"Translated to {languages[lang]['label']}\n\n{translation}"
                )


            db_lang = self.db_connector.get_language(query.from_user.id)
            if lang == db_lang:
                await query.answer()
                return

            await assign_translation_possibility(
                self,
                lang=db_lang,
                chat_id=query.from_user.id,
                message_id=query.message.id)
            await query.answer()


        async def __callback_show_all_langs(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query
            await query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(await gen_lang_buttons(show_selection=False, with_callback='trans_'))
            )
            await query.answer()

        async def __callback_pagechange(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query
            page = int(query.data.split('_')[-1])
            await query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(await gen_lang_buttons(show_selection=False, with_callback='trans_', page=page))
            )
            await query.answer()

        ptb_instance.add_handler(CallbackQueryHandler(__callback_show_all_langs, 'trans_all', block=False))
        ptb_instance.add_handler(CallbackQueryHandler(__callback_translate, 'trans_*', block=False))
        ptb_instance.add_handler(CallbackQueryHandler(__callback_pagechange, 'page_trans_*', block=False))



async def assign_translation_possibility(self,
                                         lang: str,
                                         chat_id: int,
                                         message_id: int):
    keyboard = [
        [InlineKeyboardButton('Translate to other', callback_data='trans_all')]
    ]
    if lang != 'none':
        lang_data = languages[lang]
        keyboard[0].insert(0, InlineKeyboardButton(f"Translate to {lang_data['label']}", callback_data='trans_' + lang))

    context = CallbackContext(self.ptb_instance)
    await context.bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
