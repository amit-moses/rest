from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.name}'
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, null=False)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.CharField(max_length=300, null=False, default='https://t4.ftcdn.net/jpg/04/73/25/49/360_F_473254957_bxG9yf4ly7OBO5I0O5KABlN930GwaMQz.jpg')

    def __str__(self):
        return f'{self.name}'

class Cart(models.Model):
    is_paid = models.BooleanField(default=False)
    create_date = models.DateTimeField(default=timezone.now)

class CartItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='cartitem')
    quantity = models.IntegerField(default=1)
