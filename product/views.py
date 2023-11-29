from django.shortcuts import render
from rest_framework import status
from .models import Category, Product, Cart, CartItem, Promocode
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, UserSerializer, CartItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User


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

    valid = request.user.id == cart.buyer or request.user == cart.buyer
    if request.method == 'PUT' and valid:
        cart.updatecart(params=request.data)

    elif request.method == 'DELETE' and valid:
        cart.deleteitem()

    if cart and valid:
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
        valid = request.user == cart.buyer or request.user.id == cart.buyer
        if promo == -1 and valid:
            cart.promocode = None
            cart.save()
        elif promocode and valid:
            cart.promocode = promocode.first()
            cart.save()
        if valid:
            return Response(CartSerializer(cart).data)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_cart(request):
    already_cart = request.GET.get('cart_id', 0)
    myuser = request.user
    cart = myuser.cart_set.all().filter(is_paid=False)
    if cart:
        cart = cart.order_by('-id').first()
        if not cart.cartitem.all() and already_cart:
            btd = Cart.objects.filter(pk=already_cart)
            if btd:
                cart.delete()
                cart = btd.first()
                cart.buyer = myuser
                cart.save()
    else:
        cart = Cart.objects.filter(
            pk=already_cart).first() if already_cart else Cart()
        cart.buyer = myuser
        cart.save()
    if cart:
        return Response(CartSerializer(cart).data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def register(request):
    data = JSONParser().parse(request)
    user = User.objects.create_user(
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password")
    )
    try:
        user.save()
    except Exception as e:
        return Response(e, status=400)
    return Response(UserSerializer(user).data)
