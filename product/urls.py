from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.add_get_all, name="add_get_all"),
    path('product/<int:id>/', views.one_product, name="one_product"),
    path('cart/<int:id>/', views.cart, name="cart"),
    path('cart/', views.cart, name="cart"),
    path('updatepromo/<int:id>/', views.update_promo, name="update_promo"),
    path('category/', views.categories, name="categories"),
    path('category/<int:id>/', views.one_category, name="one_category"),
    path('promo/', views.promocodes, name="promocodes"),
    path('promo/<int:id>/', views.one_promocode, name="one_promocode"),
    path('usercart/', views.get_user_cart, name="usercart"),
    path('register/', views.register, name="register"),  
]

