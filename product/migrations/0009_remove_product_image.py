# Generated by Django 4.1.10 on 2023-12-03 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_remove_product_image1_alter_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]
