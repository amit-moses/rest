from django.urls import path
from . import views

urlpatterns = [
    path('product', views.add_get_all, name="add_get_all"),
    path('product/<int:id>', views.one_prod, name="one_prod"),
    path('category', views.categories, name="categories"),    
]