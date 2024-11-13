from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm


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


def register_view(request):
    form = SignUpForm()
    context = {'form': form
               }
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            print(request.POST)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have been registered')
            return redirect('home')
        else:
            messages.success(request, 'Error. Please try again')
            return redirect('register')
    else:
        return render(request, 'register_view.html', context)


def product_view(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    return render(request, 'product_view.html', context)


def category_view(request, foo):
    foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request,'category.html', {'products': products, 'category': category})
    except:
        messages.success(request, 'The category does not exist')
        return redirect('home')










