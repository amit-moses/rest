from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.add_get_all, name="add_get_all"),
    path('product/<int:id>/', views.one_prod, name="one_prod"),
    path('cart/<int:id>/', views.cart, name="cart"),
    path('cart/', views.cart, name="cart"),
    path('category/', views.categories, name="categories"),    
]