from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('',HomeView.as_view(), name = 'home'),
    path('categories/', CategoriesView.as_view(), name = 'categories' ),
    path('product/<slug:slug>', ProductDetailView.as_view(), name='productdetail'),
    path('add-to-cart/<int:id>', AddToCartView.as_view(), name = 'addtocart'),
    path('mycart/',MyCartView.as_view(), name='mycart' ),
    path('managecart/<int:id>/', ManageCartView.as_view(), name ='managecart'),
    path('emptycart/', EmptyCartView.as_view(), name = 'emptycart'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('register/', CustomerRegistrationView.as_view(), name='register'),
    path('login/', CustomerLoginView.as_view(), name='login'),
    path('logout/', CustomerLogoutView.as_view(), name ='logout'),
    path('myprofile/', MyProfile.as_view(), name= 'myprofile'),
    path('oderdetails/<int:id>', OrderDetailsView.as_view(), name = 'orderdetails')
]
