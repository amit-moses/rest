# Generated by Django 4.1.10 on 2023-11-21 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_cart_promocode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='promocode',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
