from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('',HomeView.as_view(), name = 'home'),
    path('categories/', CategoriesView.as_view(), name = 'categories' ),
    path('product/<slug:slug>', ProductDetailView.as_view(), name='productdetail'),
    path('add-to-cart/<int:id>', AddToCartView.as_view(), name = 'addtocart')
]