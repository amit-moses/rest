from django.shortcuts import render
from rest_framework import status
import json
# Create your views here.
from django.shortcuts import render
from .models import Category, Product, Cart, CartItem, Promocode
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse


@api_view(['GET', 'POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def add_get_all(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        maxprice = request.GET.get('maxprice')
        category_filter = int(request.GET.get('category', 0))
        all_products = Product.objects.all()
        if category_filter:
            all_products = all_products.filter(category=category_filter)
        # search all product that name contains search parameter
        if search:
            all_products = all_products.filter(name__contains=search)
        # search all product that price <= maxprice (price__lte=maxprice)
        if maxprice:
            all_products = all_products.filter(price__lte=maxprice)

        all_products_json = ProductSerializer(all_products, many=True).data
        return Response(all_products_json)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["PUT", "GET", "DELETE"])
def one_prod(request, id):
    product = Product.objects.filter(pk=id)
    if product:
        product = product.first()
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(ProductSerializer(product).data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def categories(request):
    search = request.GET.get('search')
    all_categories = Category.objects.all()
    if search:
        all_categories = all_categories.filter(name__contains=search)
    all_categories_json = CategorySerializer(all_categories, many=True).data
    return Response(all_categories_json)


@api_view(["PUT", "GET", "DELETE"])
def cart(request, id=0):
    cart = Cart.objects.filter(pk=id)
    if cart:
        cart = cart.first()
        cart.promo_update()
    elif id == 0:
        cart = Cart()
        cart.save()

    if request.method == 'PUT':
        cart.updatecart(params=request.data)

    elif request.method == 'DELETE':
        cart.deleteitem()

    if cart:
        return Response(CartSerializer(cart).data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def update_promo(request, id=0):
    promo = JSONParser().parse(request).get('promocode')
    cart = Cart.objects.filter(pk=id)
    promocode = Promocode.objects.filter(code=promo).filter(used=False)
    if cart:
        cart = cart.first()
        if promo == -1:
            cart.promocode = None
            cart.save()
        elif promocode:
            cart.promocode = promocode.first()
            cart.save()
        return Response(CartSerializer(cart).data)
    return JsonResponse({})
