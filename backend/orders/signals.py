from django.db.models import Sum
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from orders.models import Coupon, Order
from orders.utils import calculate_pay_amount
from products.models import Product


@receiver(m2m_changed, sender=Order.products.through)
def m2m_products_in_order(sender, instance: Order, pk_set, **kwargs):
    if 'pre' in kwargs['action']:
        coupon = None
        if instance.offer_key is not None:
            coupon = Coupon.objects.filter(key__exact=instance.offer_key).only('is_percent', 'offer_amount').first()

        instance.sum_price = Product.objects.filter(pk__in=pk_set).aggregate(sum_price=Sum('sell_price'))['sum_price']
        instance.pay_amount = calculate_pay_amount(coupon=coupon, sum_product_price=instance.sum_price)
        instance.save(update_fields=['sum_price', 'pay_amount'])
