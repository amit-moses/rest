# Generated by Django 3.2.23 on 2023-12-04 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(default=None, max_length=300, null=True),
        ),
    ]
