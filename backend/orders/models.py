from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from orders.utils import code_coupon_key, get_payment_id
from products.models import Product

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    ORDER_STATUS = (
        ('1', 'اقدام به پرداخت'),
        ('2', 'اتمام پرداخت'),
        ('3', 'دریافت از انبار'),
        ('4', 'در حال چاپ'),
        ('5', 'آماده‌ی ارسال'),
        ('6', 'تحویل داده شده به شرکت پست'),
        ('7', 'دریافت شده توسط مشتری'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    address = models.TextField()
    postal_code = models.CharField(max_length=10, help_text="Maximum length for postal code is 10 character.")
    authority = models.CharField(max_length=36, unique=True, null=True, blank=True)
    tracking_code = models.CharField(max_length=24, unique=True, null=True, blank=True)
    pay_amount = models.PositiveIntegerField()
    payment_id = models.CharField(max_length=18, null=True, blank=True)
    status = models.CharField(choices=ORDER_STATUS, max_length=1, default='1')
    is_paid_to_provider = models.BooleanField(default=False)
    offer_key = models.CharField(max_length=32, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.payment_id}'

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = get_payment_id(self.user_id, self.product_id)
        super(Order, self).save(*args, **kwargs)


class Coupon(models.Model):
    key = models.CharField(max_length=32, unique=True, null=True, blank=True)
    is_percent = models.BooleanField(default=True)
    offer_amount = models.PositiveBigIntegerField()
    expire_date = models.DateTimeField(null=True, blank=True)
    descr = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_percent and self.offer_amount > 100:
            raise ValidationError("Invalid 'price amount'")
        if self.key is None:
            self.key = code_coupon_key(self.is_percent, self.offer_amount)
        super(Coupon, self).save(*args, **kwargs)

    def __str__(self):
        return self.key
