import logging
import os
import time
import json
import base64

from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logger = logging.getLogger(__name__)


class Connection(object):
    def __enter__(self):
        self.conn = connect(
            host="localhost",
            database=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            port=5432,
            cursor_factory=RealDictCursor
        )

        # establishing the connection
        self.conn.autocommit = True
        logging.info('-- Connection is OPEN --')
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        logger.info('-- Connection is CLOSE --')


def validate_payment_id(payment_id: str):
    spliced = payment_id.split('-')
    if len(spliced) != 3:
        return False
    if len(spliced[2]) != 8:
        return False
    return True


def check_user_validation(chat_id: int) -> bool:
    query = f"SELECT chat_id FROM accounts_user " \
            f"WHERE chat_id = '{chat_id}' " \
            f"LIMIT 1;"
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
    return len(results) == 1


def get_token_for_user(chat_id: int) -> str:
    data = {
        'chat_id': chat_id, 'timestamp': time.time(),
        'secret_key': os.getenv('TELEGRAM_BOT_SECRET_KEY'),
    }
    return base64.b64encode(json.dumps(data).encode('utf-8')).decode('utf-8')


def activate_user(chat_id: int, update):
    token = get_token_for_user(chat_id)
    keyboard = [
        [
            InlineKeyboardButton('فعالسازی', url=f'https://scarfly.ir/activate/?token={token}')
        ]
    ]
    update.message.reply_text("برای فعالسازی من، روی دکمه ی زیر کلیک کنید.", reply_markup=InlineKeyboardMarkup(keyboard))
