# Generated by Django 4.0.2 on 2022-04-21 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_pay_amount_alter_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='price_amount',
            new_name='offer_amount',
        ),
    ]
