# Generated by Django 4.0.2 on 2022-04-27 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_order_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='sum_price',
            field=models.PositiveIntegerField(default=12000),
            preserve_default=False,
        ),
    ]