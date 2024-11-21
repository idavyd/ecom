from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
# from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    context = {'cart_products': cart_products,
               'quantities': quantities}
    return render(request, 'cart_summary.html', context)


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        number_of_prod_in_cart = int(request.POST.get('product_quantity'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product, number_of_prod_in_cart)
        cart_quantity = cart.__len__()
        #response = JsonResponse({'Product_name': product.name})
        response = JsonResponse({'cart_quantity': cart_quantity})
        print('Product added to the cart')
        return response






def cart_delete(request):
    return render(request, 'about_view.html', {})


def cart_update(request):
    return render(request, 'about_view.html', {})


