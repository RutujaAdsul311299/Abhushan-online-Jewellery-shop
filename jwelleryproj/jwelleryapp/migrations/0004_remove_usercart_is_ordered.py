# Generated by Django 5.0.3 on 2024-03-11 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jwelleryapp', '0003_order_order_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercart',
            name='is_ordered',
        ),
    ]