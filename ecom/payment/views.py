from django.shortcuts import render
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    total = cart.total()
    if request.user.is_authenticated:
        s_user = ShippingAddress.objects.get(user__id=request.user.id)
        s_form = ShippingForm(request.POST or None, instance=s_user)
        context = {'cart_products': cart_products,
                   'quantities': quantities,
                   'total': total,
                   's_form': s_form
                   }
        return render(request, 'payment/checkout.html', context)
    else:
        s_form = ShippingForm(request.POST or None)
        context = {'cart_products': cart_products,
                   'quantities': quantities,
                   'total': total,
                   's_form': s_form
                   }
        return render(request, 'payment/checkout.html', context)


