# Generated by Django 4.2.6 on 2024-01-28 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='channel',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processed', 'Processed'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default=('Pending', 'Pending'), max_length=50),
        ),
        migrations.AddField(
            model_name='payment',
            name='transaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
