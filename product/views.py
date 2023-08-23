from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser


@api_view()
def products(request):        
    search = request.GET.get('search')
    maxprice = request.GET.get('maxprice')
    all_products = Product.objects.all()
    # search all product that name contains search parameter
    if search:
        all_products = all_products.filter(name__contains=search)
    # search all product that price <= maxprice (price__lte=maxprice)
    if maxprice:
        all_products = all_products.filter(price__lte=maxprice)

    all_products_json = ProductSerializer(all_products, many=True).data
    return Response(all_products_json)


"""
in create_product we get a POST request containing a json
 {
    "name": "Picture Frame",
    "price": "29.00",
    "stock": 150
}
"""
@api_view(["POST","GET"])
def add_get_all(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        maxprice = request.GET.get('maxprice')
        all_products = Product.objects.all()
        # search all product that name contains search parameter
        if search:
            all_products = all_products.filter(name__contains=search)
        # search all product that price <= maxprice (price__lte=maxprice)
        if maxprice:
            all_products = all_products.filter(price__lte=maxprice)

        all_products_json = ProductSerializer(all_products, many=True).data
        return Response(all_products_json)
    elif request.methods == 'POST':
        # this line parses the json from request
        data = JSONParser().parse(request)
        # this line creates a serializer object from json data
        serializer = ProductSerializer(data=data)
        # this line checkes validity of json data 
        if serializer.is_valid():
            # the serializer.save - saves a new product object
            serializer.save()
            # returns the object that was created including id
            return Response(serializer.data, status=201)
        # if not valid. return errors.
        return Response(serializer.errors, status=400)  


@api_view(["PUT","GET", "DELETE"])
def one_prod(request, id):
    product = Product.objects.filter(pk = id)
    if request.method == 'GET':
        return Response(ProductSerializer(product, many = True).data)
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
    

@api_view()
def categories(request):
    search = request.GET.get('search')
    all_categories = Category.objects.all()
    if search:
        all_categories = all_categories.filter(name__contains=search)
    all_categories_json = CategorySerializer(all_categories, many=True).data
    return Response(all_categories_json)