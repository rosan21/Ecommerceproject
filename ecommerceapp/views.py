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
    template_name ='addtocart.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
    	#get product id
        product_id = self.kwargs['id']

        #get product
        product = Product.objects.get(id = product_id)

        #check if cart exists
        card_id = self.request.session.get('cart_id', None)
        
        


        return context