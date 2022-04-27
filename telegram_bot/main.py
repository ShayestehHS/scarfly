#!/usr/bin/env python
import logging
import sys
import os
from pathlib import Path
from telegram import Update
from telegram.ext import (
    Filters, MessageHandler, Updater,
    CommandHandler, ConversationHandler, CallbackContext,
)

myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
a = str(path.parent.absolute())

sys.path.append(a)
from telegram_bot.utils import Connection, activate_user, check_user_validation, validate_payment_id

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot_token = os.getenv('TELEGRAM_BOT_BOT_TOKEN')
ORDER_STATUS = (
    'اقدام به پرداخت',
    'اتمام پرداخت',
    'دریافت از انبار',
    'در حال چاپ',
    'آماده‌ی ارسال',
    'تحویل داده شده به شرکت پست',
    'دریافت شده توسط مشتری',
)
# Stages
STATUS_FIRST, STATUS_SECOND = range(2)
# Callback data
ONE, TWO, THREE, FOUR = range(4)
STATUS_ONE = 0


def start(update: Update, context: CallbackContext):
    logger.info(f"Function: start             User:{update.message.from_user.username}")
    chat_id = update.message.chat_id
    is_user_valid = check_user_validation(chat_id)
    if not is_user_valid:
        activate_user(chat_id, update)
        return

    update.message.reply_text("برای استفاده از من، میتونید از گزینه های زیر استفاده کنید:"
                              "\n/start شروع ربات"
                              "\n/status دریافت وضعیت مرسوله"
                              "\n/cancel لغو فرایند جاری")


def status(update: Update, context: CallbackContext) -> int:
    logger.info(f"Function: status            User:{update.message.from_user.username}")
    update.message.reply_text(text="کد رهگیری ای که ما به شما دادیم را وارد کنید...")
    return STATUS_SECOND


def status_get_payment_id(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    if not check_user_validation(chat_id):
        update.message.reply_text("شما در ابتدا باید من را فعال کنید تا شما رو بشناسم و از شما دستور بگیرم.")
        activate_user(chat_id, update)
        return ConversationHandler.END
    payment_id = update.message.text
    is_valid = validate_payment_id(payment_id)
    if not is_valid:
        update.message.reply_text("این کد از نظر من درست نیست.\nلطفا دوباره کد رو بررسی کن و برام بفرست.\nاگر هم میخوای میتونی این فرایند رو متوقف کنی.\n /cancel")
        return STATUS_SECOND

    subquery = f"SELECT id FROM accounts_user as au WHERE au.chat_id = '{chat_id}'"
    query = f"SELECT status FROM orders_order " \
            f"INNER JOIN accounts_user au on orders_order.user_id = au.id " \
            f"WHERE orders_order.payment_id = '{payment_id}' " \
            f"AND orders_order.user_id = ({subquery})"
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
    if len(results) == 0:
        update.message.reply_text('کد وارد شده، صحیح نمی باشد.\nلطفا کد وارد شده را بررسی نمایید و دوباره ارسال کنید.\nدر غیر اینصورت فرایند جاری را متوقف کنید.\n /cancel')
        return STATUS_SECOND
    status_description = ORDER_STATUS[int(results[0]['status']) - 1]
    update.message.reply_text(f"وضعيت مرسوله ي شما در وضعيت زير قرار دارد:\n {status_description}")
    return ConversationHandler.END


def status_end(update: Update, context: CallbackContext) -> int:
    logger.info(f"Function: status_end        User:{update.message.from_user.username}")
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="امیدوارم دوباره بتونم کمک تون كنم ☺")
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    logger.info(f"Function: cancel            User:{update.message.from_user.username}")
    update.message.reply_text('فرمان شما دریافت شد.\n'
                              ' موفق باشی دوست من.')

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('status', status)],
        states={
            STATUS_FIRST: [MessageHandler(Filters.text & ~Filters.command, status)],
            STATUS_SECOND: [MessageHandler(Filters.text & ~Filters.command, status_get_payment_id)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
