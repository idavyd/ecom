# Generated by Django 5.1.3 on 2024-12-02 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_rename_address1_order_shipping_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_shipped',
            field=models.BooleanField(default=False),
        ),
    ]
