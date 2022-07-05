from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View,CreateView
from ecommerceapp.models import Product,Category, Cart, CartProduct
from .forms import CheckOutForm


# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['products'] = Product.objects.all()
        
         return context

class CategoriesView(TemplateView):
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductDetailView(TemplateView):
    template_name = 'productdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product= Product.objects.get(slug = url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product

        return context

class AddToCartView(TemplateView):
    template_name = 'addtocart.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        product_id = self.kwargs['id']
        product_object = Product.objects.get(id=product_id)

        cart_id = self.request.session.get('cart_id',None )
        #check if cart exists
        if cart_id:
            cart_object = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_object.cartproduct_set.filter(product=product_object)
            #checking if the product already exists in the cart and if it exists
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal +=product_object.selling_price
                cartproduct.save()
                cart_object.total += product_object.selling_price
                cart_object.save()
            #new product added to cart
            else:
                cartproduct= CartProduct.objects.create(cart=cart_object, product=product_object,rate=product_object.selling_price,quantity=1,subtotal=product_object.selling_price)
                cart_object.total += product_object.selling_price
                cart_object.save()
        #if cart doesnot exist
        else:
            cart_object = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_object.id
            cartproduct= CartProduct.objects.create(cart=cart_object, product=product_object,rate=product_object.selling_price,quantity=1,subtotal=product_object.selling_price)
            cart_object.total += product_object.selling_price
            cart_object.save()

        return context

class MyCartView(TemplateView):
    template_name ='mycart.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        
        if cart_id:
            cart_object = Cart.objects.get(id=cart_id)
        else:
            cart_object =None
        context['cart']=cart_object


        return context

class ManageCartView(View):
    def get(self, request,id, *args, **kwargs):
        cart_product_object = CartProduct.objects.get(id=id)
        cart_object = cart_product_object.cart
        cart_action = request.GET.get('action')
        if cart_action == 'inc':
            cart_product_object.quantity+=1
            cart_product_object.subtotal+=cart_product_object.rate
            cart_product_object.save()
            cart_object.total +=cart_product_object.rate
            cart_object.save()
        elif cart_action == 'dec':
            cart_product_object.quantity-=1
            cart_product_object.subtotal-=cart_product_object.rate
            cart_product_object.save()
            cart_object.total -=cart_product_object.rate
            cart_object.save()
            if cart_product_object.quantity == 0:
                cart_product_object.delete()
        elif cart_action == 'rmv':
            cart_object.total-= cart_product_object.subtotal
            cart_object.save()
            cart_product_object.delete()
            
        else:
            return redirect('mycart')

        return redirect('mycart')

class EmptyCartView(View):
    def get(self,request, *args, **kwargs):
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart_object = Cart.objects.get(id=cart_id)
            cart_object.cartproduct_set.all().delete()
            cart_object.total = 0
            cart_object.save()
            return redirect('mycart')
        return redirect('mycart')

class CheckOutView(CreateView):
    template_name = 'checkout.html'
    form_class = CheckOutForm
    success_url= reverse_lazy('home')
    
    

    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id')
        cart_object = Cart.objects.get(id=cart_id)
        context['cart'] = cart_object

        return context