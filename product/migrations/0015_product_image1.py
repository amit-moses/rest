# Generated by Django 4.1.10 on 2023-12-04 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image1',
            field=models.ImageField(default='products_images/default.jpg', upload_to='products_images'),
        ),
    ]
