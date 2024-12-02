from django.shortcuts import render
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress
from django.contrib import messages
from django.shortcuts import redirect, render


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


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        total = cart.total()
        s_user = ShippingAddress.objects.get(user__id=request.user.id)
        s_info = ShippingForm(request.POST or None, instance=s_user)
        billing_form = PaymentForm()
        context = {'cart_products': cart_products,
                   'quantities': quantities,
                   'total': total,
                   's_info': request.POST,
                   'billing_form': billing_form
                   }
        if request.user.is_authenticated:
            return render(request, 'payment/billing_info.html', context)
        else:
            return render(request, 'payment/billing_info.html', context)

    else:
        print(request.META.get('HTTP_REFERER'))
        messages.success(request, 'No no no can not do that')
        return redirect('home')


