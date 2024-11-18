from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
# from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    return render(request, 'cart_summary.html', {})


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product,id=product_id)
        cart.db_add(product)
        cart_quantity = cart.__len__()
        #response = JsonResponse({'Product_name': product.name})
        response = JsonResponse({'cart_quantity': cart_quantity})
        print('prod added')
        return response






def cart_delete(request):
    return render(request, 'about_view.html', {})


def cart_update(request):
    return render(request, 'about_view.html', {})


