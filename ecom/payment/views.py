from django.shortcuts import render
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from store.models import Product, Profile
import datetime as dt



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
        billing_form = PaymentForm()
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        context = {'cart_products': cart.get_prods(),
                   'quantities': cart.get_quants(),
                   'total': cart.total(),
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
        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')
        shipping_address = (f"{my_shipping['shipping_address1']}\n"
                            f"{my_shipping['shipping_address2']}\n"
                            f"{my_shipping['shipping_city']}\n"
                            f"{my_shipping['shipping_state']}\n"
                            f"{my_shipping['shipping_zipcode']}\n"
                            f"{my_shipping['shipping_country']}\n")

        if request.user.is_authenticated:
            new_order = Order(user=request.user,
                              full_name=my_shipping['shipping_full_name'],
                              email=my_shipping['shipping_email'],
                              amount_paid=cart.total(),
                              shipping_address=shipping_address)
            new_order.save()
            order_id = new_order.pk
            for product in cart.get_prods():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                for key, value in cart.get_quants().items():
                    if int(key) == product.id:
                        quantity = value
                        create_order_item = OrderItem(order_id=order_id,
                                                      product_id=product_id,
                                                      user=request.user,
                                                      quantity=quantity,
                                                      price=price)
                        create_order_item.save()
            cart.clear()
            current_user = Profile.objects.filter(user__id=request.user.id)
            current_user.update(old_cart='')
            messages.success(request, 'Order Placed!')
            return redirect('home')
        else:
            new_order = Order(
                full_name=my_shipping['shipping_full_name'],
                email=my_shipping["shipping_email"],
                amount_paid=cart.total(),
                shipping_address=shipping_address)
            new_order.save()
            order_id = new_order.pk

            for product in cart.get_prods():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key, value in cart.get_quants().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id,
                                                      product_id=product_id,
                                                      quantity=value,
                                                      price=price)
                        create_order_item.save()
            cart.clear()
            messages.success(request, 'Order Placed!')
            return redirect('home')
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.POST:
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            order.update(is_shipped=False, date_shipped=None)
            messages.success(request, 'Marked as unshipped')
            return redirect('unshipped_dash')
        orders = Order.objects.filter(is_shipped=True)
        context = {'orders': orders}
        return render(request, 'payment/shipped_dash.html', context)
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(is_shipped=False)
        if request.POST:
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            order.update(is_shipped=True, date_shipped=dt.datetime.now())
            messages.success(request, 'Marked as shipped')
            return redirect('shipped_dash')
        context = {'orders': orders}
        return render(request, 'payment/not_shipped_dash.html', context)
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        if request.POST:
            status = request.POST['shipping_status']
            if status == 'true':
                order = Order.objects.filter(id=pk)
                order.update(is_shipped=True, date_shipped=dt.datetime.now())
                messages.success(request, 'Marked as shipped')
                return redirect('shipped_dash')
            else:
                order = Order.objects.filter(id=pk)
                order.update(is_shipped=False, date_shipped=None)
                messages.success(request, 'Marked as unshipped')
                return redirect('not_shipped_dash')
        context = {'order': order,
                   'items': items}
        return render(request, 'payment/orders.html', context)

    else:
        messages.success(request, 'Access Denied')
        return redirect('home')
