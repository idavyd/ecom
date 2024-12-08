from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
# from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    total = cart.total()
    context = {'cart_products': cart_products,
               'quantities': quantities,
               'total': total}
    return render(request, 'cart_summary.html', context)


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        number_of_prod_in_cart = int(request.POST.get('product_quantity'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product, number_of_prod_in_cart)
        cart_quantity = cart.__len__()
        # response = JsonResponse({'Product_name': product.name})
        response = JsonResponse({'cart_quantity': cart_quantity})
        messages.success(request, 'Product added to the cart')
        print('Product added to the cart')
        return response


def delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product=product)
        messages.success(request, 'Product removed from the cart')
        #response = JsonResponse({'product': product})
        return redirect('cart_summary')


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_quantity'))
        old_q = cart.cart[f'{str(product_id)}']
        cart.update(product_id, product_qty)
        response = JsonResponse({'product_qty': product_qty})
        messages.success(request, 'Cart updated!')
        print(f'q of item {product_id} updated from {old_q} to {product_qty} ')
        return response


