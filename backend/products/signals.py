from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from telegram import Bot
from telegram.error import BadRequest

from products.models import Product

TELEGRAM_TOKEN = settings.TELEGRAM['bot_token']
TELEGRAM_CHANNEL_USERNAME = settings.TELEGRAM['channel_username']


@receiver(pre_delete, sender=Product)
def delete_post_from_channel(sender, instance: Product, using, **kwargs):
    if instance.channel_message_id:
        try:
            bot = Bot(token=TELEGRAM_TOKEN)
            bot.delete_message(chat_id=TELEGRAM_CHANNEL_USERNAME, message_id=instance.channel_message_id)
        except BadRequest as e:
            if e.message.lower() != "Message to delete not found".lower():
                raise e
