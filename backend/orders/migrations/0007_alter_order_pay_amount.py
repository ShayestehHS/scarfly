# Generated by Django 3.2.13 on 2022-04-28 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_postal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pay_amount',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]