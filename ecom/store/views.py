from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home_view(request):
    products = Product.objects.all()
    context = {'products': products
    }
    return render(request, 'home_view.html', context)


def about_view(request):
    return render(request, 'about_view.html', {})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in')
            return redirect('home')
        else:
            messages.error(request, 'There was an error. Please try again')
            return redirect('login')
    else:
        return render(request, 'login_view.html', {})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')



