import messages

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from telegram.ext import ContextTypes, CommandHandler, Application, MessageHandler, filters, PreCheckoutQueryHandler, \
    CallbackQueryHandler, ConversationHandler

from database import DBConnector


class __Payments:
    def __init__(self, ptb_instance: Application,
                 db_connector: DBConnector,
                 payment_token: str):

        async def top_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Select an option!\nYou can also leave a tip inside the invoice!",
                                           reply_markup=InlineKeyboardMarkup(
                                               [
                                                   [InlineKeyboardButton("1.800 CR\n(1€ / 30 m)",
                                                                         callback_data="top_balance-1800"),
                                                     InlineKeyboardButton("3.600 CR\n(2€ / 1 H)",
                                                                         callback_data="top_balance-3600")],
                                                   [InlineKeyboardButton("9.000 CR\n(5€ / 2.5 h)",
                                                                         callback_data="top_balance-9000"),
                                                    InlineKeyboardButton("18.000 CR\n(10€ / 5 h)",
                                                                         callback_data="top_balance-18000")]
                                               ]
                                           ))

        async def tip_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=messages.tip,
                                           parse_mode="Markdown",
                                           reply_markup=InlineKeyboardMarkup(
                                               [
                                                   [InlineKeyboardButton("1€ (some fries 🍟)",
                                                                         callback_data="tip-100"),
                                                     InlineKeyboardButton("5€ (1 BK menu 🍔)",
                                                                         callback_data="tip-500")],
                                                   [InlineKeyboardButton("10€ (1 Special BK menu 🍔🍟)",
                                                                         callback_data="tip-1000"),
                                                    InlineKeyboardButton("20€ (Dinner for 2 🍔🍔🍟)",
                                                                         callback_data="tip-2000")]
                                               ]
                                           ))


        async def top_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query
            amount = int(query.data.split('-')[-1])

            try:
                price = amount // 18

                await context.bot.send_invoice(
                    chat_id=query.from_user.id,
                    title="Credits",
                    description="Buying " + str(amount) + " credits",
                    payload="credits",
                    provider_token=payment_token,
                    currency="EUR",
                    prices=[LabeledPrice( str(amount) + " credits", price)],
                    max_tip_amount=5000,
                    suggested_tip_amounts=[100, 300, 500, 1000]
                )

                await query.answer()
                return ConversationHandler.END

            except Exception as e:
                print(e.with_traceback())
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text="Error creating invoice. Please contact @TeleWhisperSupport")

                await query.answer()

        async def tipping(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query
            amount = int(query.data.split('-')[-1])

            try:
                price = amount

                await context.bot.send_invoice(
                    chat_id=query.from_user.id,
                    title="Tip",
                    description="Blessing the dev with " + str(amount) + " cents",
                    payload="tip",
                    provider_token=payment_token,
                    currency="EUR",
                    prices=[LabeledPrice("Base tip", price)],
                    max_tip_amount=5000,
                    suggested_tip_amounts=[100, 300, 500, 1000]
                )

                await query.answer()
                return ConversationHandler.END

            except Exception as e:
                print(e.with_traceback())
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text="Error creating invoice. Please contact @TeleWhisperSupport")

                await query.answer()


        async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            query = update.pre_checkout_query
            try:
                # check the payload, is this from your bot?
                if query.invoice_payload != "tip" and query.invoice_payload != "credits":
                    # answer False pre_checkout_query
                    await query.answer(ok=False, error_message="Something went wrong...")

                else:
                    await query.answer(ok=True)

            except Exception as e:
                await query.answer(ok=False, error_message="Something went wrong...")

        async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            try:
                user_id = update.message.from_user.id
                if update.message.successful_payment.invoice_payload == "credits":
                    await db_connector.register_transaction(
                        user_id=user_id,
                        amount=(update.message.successful_payment.total_amount * 18)
                    )
                    await update.message.reply_text(
                        str(update.message.successful_payment.total_amount * 18) + " credits added to your account 💸")

                await update.message.reply_text("Thank you for your support! ❤️‍🔥")

            except Exception as e:
                print(e)
                await update.message.reply_text("Error processing payment. Please contact @TeleWhisperSupport for refund if necessary")

        top_balance_handler = CommandHandler('top_balance', top_options, block=False, filters=filters.ChatType.PRIVATE)
        tip_balance_handler = CommandHandler('tip', tip_options, block=False, filters=filters.ChatType.PRIVATE)
        checkout_handler = PreCheckoutQueryHandler(precheckout_callback, block=False)
        success_handler = MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback, block=False)

        inline_credit_handler = CallbackQueryHandler(top_balance, pattern=r'top_balance-\d+', block=False)
        inline_tip_handler = CallbackQueryHandler(tipping, pattern=r'tip-\d+', block=False)

        ptb_instance.add_handler(top_balance_handler)
        ptb_instance.add_handler(tip_balance_handler)
        ptb_instance.add_handler(checkout_handler)
        ptb_instance.add_handler(success_handler)
        ptb_instance.add_handler(inline_credit_handler)
        ptb_instance.add_handler(inline_tip_handler)
