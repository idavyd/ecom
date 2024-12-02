from django.shortcuts import render
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from store.models import Product


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
        billing_form = PaymentForm()
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
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


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        total = cart.total()
        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')
        print(my_shipping)
        shipping_address = (f"{my_shipping['shipping_address1']}\n"
                            f"{my_shipping['shipping_address2']}\n"
                            f"{my_shipping['shipping_city']}\n"
                            f"{my_shipping['shipping_state']}\n"
                            f"{my_shipping['shipping_zipcode']}\n"
                            f"{my_shipping['shipping_country']}\n")
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        amount_paid = total
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user,
                                 full_name=full_name,
                                 email=email,
                                 amount_paid=amount_paid,
                                 shipping_address=shipping_address)
            create_order.save()
            order_id = create_order.pk
            for product in cart_products:
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                for key, value in quantities.items():
                    if int(key) == product.id:
                        quantity = value
                        create_order_item = OrderItem(order_id=order_id,
                                                      product_id=product_id,
                                                      user=user,
                                                      quantity=quantity,
                                                      price=price)
                        create_order_item.save()
            messages.success(request, 'Order Placed!')
            return redirect('home')
        else:
            create_order = Order(
                                 full_name=full_name,
                                 email=email,
                                 amount_paid=amount_paid,
                                 shipping_address=shipping_address)
            create_order.save()
            order_id = create_order.pk
            for product in cart_products:
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                for key, value in quantities.items():
                    if int(key) == product.id:
                        quantity = value
                        create_order_item = OrderItem(order_id=order_id,
                                                      product_id=product_id,
                                                      quantity=quantity,
                                                      price=price)
                        create_order_item.save()
            messages.success(request, 'Order Placed!')
            return redirect('home')
    else:
        print(request.META.get('HTTP_REFERER'))
        messages.success(request, 'No no no can not do that')
        return redirect('home')


