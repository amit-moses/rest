from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from firebase_admin import storage


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
    image = models.CharField(max_length=300, null=True, default='default')
    # image = models.ImageField(upload_to='products_images', default='products_images/default.jpg')
    
    def delete(self, *args, **kwargs):
        # Print the value of the 'name' field before deletion
        print(f"Deleting instance with name: {self.name}")

        if self.image and self.image != 'default':
            bucket = storage.bucket()
            blob = bucket.blob(self.image)
            blob.delete()
        # Perform the actual delete operation
        super(Product, self).delete(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
    
     
    
class Promocode(models.Model):
    code = models.CharField(max_length=100, null=True, default=None)
    used = models.BooleanField(default=False)
    discount = models.IntegerField(default=0)

class Cart(models.Model):
    is_paid = models.BooleanField(default=False)
    create_date = models.DateTimeField(default=timezone.now)
    promocode = models.ForeignKey(Promocode, on_delete=models.CASCADE, null=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def total_to_pay(self):
        percent_to_pay = 100
        if self.promocode:
            if not self.promocode.used:
                percent_to_pay -= min(100,self.promocode.discount)

        total_price = 0
        for item in self.cartitem.all():
            total_price += item.get_total()
        return round(float(total_price) * (max(percent_to_pay,0) / 100),2)
    
    def total_before(self):
        total_price = 0
        for item in self.cartitem.all():
            total_price += item.get_total()
        return total_price

    def deleteitem(self):
        self.cartitem.all().delete()

    def get_buyer(self):
        return self.buyer.username if self.buyer else None
        # return self.buyer.id if self.buyer else None
    
    def promo_update(self): 
        if self.promocode:
            if self.promocode.used and not self.is_paid: 
                self.promocode = None
                self.save()
        

    def updatecart(self, params):
        data = params
        cartitem = self.cartitem.filter(product_id = data.get('product'))
        if cartitem:
            cartupdate = cartitem.first()
            new_quantity = cartupdate.quantity + int(data.get('quantity'))
            if 0 < new_quantity:
                if new_quantity <= cartupdate.product.stock:
                    cartupdate.quantity = new_quantity 
                    cartupdate.save()
            else: cartupdate.delete()
        else: 
            CartItem(product_id = data.get('product'), quantity=data.get('quantity'), cart_id = self.id).save()

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='cartitem')
    quantity = models.IntegerField(default=1)

    def get_total(self):
        rtn = self.quantity * self.product.price
        if rtn < 0:
            self.delete()
        return rtn if 0<rtn else 0






