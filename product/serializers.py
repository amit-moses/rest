from rest_framework import serializers
from .models import Category, Product
        
class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(many=False, read_only=True)
    class Meta:
        model = Product
        fields = '__all__' 
        # example of how to filter fields. remove line 7 __all__ and replace with line 9:
        # fields = ['name','price']

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__' 

