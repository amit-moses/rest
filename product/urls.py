from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.add_get_all, name="add_get_all"),
    path('product/<int:id>/', views.one_prod, name="one_prod"),
    path('cart/<int:id>/', views.cart, name="cart"),
    path('cart/', views.cart, name="cart"),
    path('updatepromo/<int:id>/', views.update_promo, name="update_promo"),
    path('category/', views.categories, name="categories"),
    path('category/<int:id>/', views.one_cat, name="one_cat"),
    path('promo/', views.promocodes, name="promocodes"),
    path('promo/<int:id>/', views.one_pro, name="one_pro"),
    path('usercart/', views.get_user_cart, name="usercart"),
    path('register/', views.register, name="register"),  
]

