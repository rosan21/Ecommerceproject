from django.contrib import admin
from .models import Customer,Cart,CartProduct,Category,Product,Order, Admin

# Register your models here.

class CartProductAdmin(admin.TabularInline):
    model=CartProduct

class OrderAdmin(admin.TabularInline):
    model=Order

class CartAdmin(admin.ModelAdmin):
    
    inlines=[CartProductAdmin,OrderAdmin]

admin.site.register([Customer,Category,Product, Admin])

admin.site.register(Cart,CartAdmin)