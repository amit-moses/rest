# Generated by Django 4.1.10 on 2023-12-03 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='products_images/default.jpg', null=True, upload_to='products_images'),
        ),
    ]
