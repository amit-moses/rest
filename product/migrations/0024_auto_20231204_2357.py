# Generated by Django 3.2.23 on 2023-12-04 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_rename_image_product_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_image',
        ),
        migrations.AddField(
            model_name='product',
            name='product_image1',
            field=models.CharField(default=None, max_length=300, null=True),
        ),
    ]
