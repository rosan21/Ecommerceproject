from django.contrib import admin
from .models import Customer,Cart,CartProduct,Category,Product

# Register your models here.

admin.site.register([Customer,Cart,CartProduct,Category,Product])