# Generated by Django 3.2.13 on 2022-04-28 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_pay_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='sum_price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
