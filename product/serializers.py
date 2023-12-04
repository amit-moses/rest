from rest_framework import serializers
from .models import Category, Product, CartItem, Cart, Promocode
from django.contrib.auth.models import User
from django.utils import timezone



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    carts = serializers.SerializerMethodField()
    applied = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'carts', 'applied', 'last_login','is_staff')
    
    def get_carts(self, obj):
        return len(obj.cart_set.filter(cartitem__isnull=False).all())
    
    def get_applied(self, obj):
        return obj.date_joined
    
    def get_last_login(self, obj):
        return obj.last_login

    
class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(many=False, read_only=True)
    # products_images/default.jpg
    class Meta:
        model = Product
        fields = '__all__'
        


class CategorySerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'

class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    cartitem = CartItemSerializer(many=True, read_only=True)
    promocode = PromoSerializer(many=False, read_only=True)
    total = serializers.SerializerMethodField()
    total_before = serializers.SerializerMethodField()
    buyer = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_buyer(self, obj):
        return obj.get_buyer()
    
    def get_total(self, obj):
        return obj.total_to_pay()
    
    def get_total_before(self, obj):
        return obj.total_before()



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        user.last_login = timezone.now()
        user.save()
        cart = user.cart_set.all().filter(is_paid = False)
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        token['cart_id'] = cart.order_by('-id').first().id if cart else 0
        return token