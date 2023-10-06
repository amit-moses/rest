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

    def total_to_pay(self):
        total_price = 0
        for item in self.cartitem.all():
            total_price += item.get_total()
        return total_price
    
    def deleteitem(self):
        self.cartitem.all().delete()
            
    def updatecart(self, params):
        data = params
        cartitem = self.cartitem.filter(product_id = data.get('product'))
        if cartitem:
            cartupdate = cartitem.first()
            cartupdate.quantity += int(data.get('quantity'))
            if cartupdate.quantity <= cartupdate.product.stock and cartupdate.quantity > 0: cartupdate.save()
            elif cartupdate.quantity == 0: cartupdate.delete()
        else: 
            CartItem(product_id = data.get('product'), quantity=data.get('quantity'), cart_id = self.id).save()

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='cartitem')
    quantity = models.IntegerField(default=1)

    def get_total(self):
        return self.quantity * self.product.price
