from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from telegram import Bot, Message
from telegram.constants import PARSEMODE_MARKDOWN_V2
from telegram.error import BadRequest

User = settings.AUTH_USER_MODEL
TELEGRAM_TOKEN = settings.TELEGRAM['bot_token']
TELEGRAM_CHANNEL_USERNAME = settings.TELEGRAM['channel_username']
SCARFLY_FULL_URL = settings.TELEGRAM['full_url']


def product_image_path(instance, filename):
    return f'products/{instance.pro_code}/{filename}'


class Product(models.Model):
    name = models.CharField(max_length=64)
    pro_code = models.PositiveSmallIntegerField(unique=True)
    image = models.ImageField(upload_to=product_image_path)
    instagram_url = models.URLField()
    channel_message_id = models.PositiveIntegerField(null=True, blank=True)
    sell_price = models.PositiveIntegerField(help_text="Enter the amount in Rial")
    buy_price = models.PositiveIntegerField(help_text="Enter the amount in Rial")
    description = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.pro_code}"

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        if self.sell_price < self.buy_price:
            raise ValidationError("Sell price should be greater that buy price")

        if self.description:
            bot = Bot(token=TELEGRAM_TOKEN)
            caption = f"نام محصول: {self.name} \n" \
                      f"کد محصول: {self.pro_code} \n" \
                      f"وضعیت موجودی: {'موجود' if self.is_available else 'ناموجود'} \n" \
                      f"توضیحات محصول: {self.description}\n\n\n" \
                      f"[مشاهده در اینستاگرام]({self.instagram_url})\n" \
                      fr"@scarfly\_admin ارتباط با ادمین"

            if not self.channel_message_id:
                # Send the post to channel and update the 'channel_message_id' field
                message: Message = bot.send_photo(chat_id=TELEGRAM_CHANNEL_USERNAME, caption=caption,
                                                  parse_mode=PARSEMODE_MARKDOWN_V2,
                                                  photo=f"{SCARFLY_FULL_URL}{self.image.url}")

                self.channel_message_id = message.message_id
                self.save(update_fields=['channel_message_id'])

            else:
                # Update the related post from channel
                try:
                    bot.edit_message_caption(chat_id=TELEGRAM_CHANNEL_USERNAME,
                                             message_id=self.channel_message_id,
                                             caption=caption, parse_mode=PARSEMODE_MARKDOWN_V2)
                except BadRequest as e:
                    if 'Message is not modified'.lower() not in e.message.lower():
                        raise e
