# Generated by Django 5.0.3 on 2024-03-11 16:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwelleryapp', '0002_remove_usercart_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]