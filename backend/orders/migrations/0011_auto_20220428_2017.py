# Generated by Django 3.2.13 on 2022-04-28 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20220428_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pay_amount',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='sum_price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]