# Generated by Django 4.2.6 on 2024-01-28 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0002_payment_channel_payment_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='channel',
            field=models.CharField(choices=[('mobile_money', 'mobile_money')], default=('mobile_money', 'mobile_money'), max_length=50),
        ),
        migrations.AlterField(
            model_name='payment',
            name='ref',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
