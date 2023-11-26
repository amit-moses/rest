from rest_framework import serializers
from .models import Category, Product, CartItem, Cart, Promocode


class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(many=False, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        # example of how to filter fields. remove line 7 __all__ and replace with line 9:
        # fields = ['name','price']


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
