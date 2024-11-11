from django.shortcuts import render
from .models import Product


def home_view(request):
    return render(request, 'home_view.html', {})


