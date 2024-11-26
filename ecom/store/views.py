from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.db.models import Q


def home_view(request):
    products = Product.objects.all().order_by('category')
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


def product_view(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    return render(request, 'product_view.html', context)


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
            messages.success(request, 'Username created. Please fill out your billing info')
            return redirect('update_info')
        else:
            messages.success(request, 'Error. Please try again')
            return redirect('register')
    else:
        return render(request, 'register_view.html', context)


def category_view(request, foo):
    foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.success(request, 'The category does not exist')
        return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    context = {'categories': categories
    }
    return render(request, 'category_summary.html', context)


def update_user(request):
    if request.user.is_authenticated:
        form = UpdateUserForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()
            login(request, request.user)
            messages.success(request, 'Сосать хуй!')
            return redirect('home')
        return render(request, 'update_user.html', {'form': form})
    else:
        messages.success(request, 'YOu must be logged in to access that page')
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        password_form = ChangePasswordForm(user=request.user)
        if request.method == 'POST':
            password_form = ChangePasswordForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Password has been updated')
                return redirect('update_user')
            else:
                for err in list(password_form.errors.values()):
                    messages.error(request, err)
                    return redirect('update_password')
        else:
            return render(request, 'update_password.html', {'password_form': password_form})
    else:
        messages.success(request, 'YOu must be logged in to access that page')
        return redirect('home')


def update_info(request):
    if request.user.is_authenticated:
        profile_needed = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=profile_needed)
        if form.is_valid():
            form.save()
            messages.success(request, 'Info has been update!')
            return redirect('home')
        return render(request, 'update_info.html', {'form': form})
    else:
        messages.success(request, 'YOu must be logged in to access that page')
        return redirect('home')


def search(request):
    if request.method == 'POST':
        searched = Product.objects.filter(Q(name__icontains=request.POST['searched'])
                                          | Q(description__icontains=request.POST['searched']))
        if not searched:
            messages.success(request, 'That product does not exist')
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})







