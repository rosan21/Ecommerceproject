from django.shortcuts import render
from django.views.generic import TemplateView
from ecommerceapp.models import Product,Category, Cart, CartProduct


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