from django.contrib import admin
from .models import Category, Customer, Product, Order


models = [Category, Customer, Product, Order]

for model in models:
    admin.site.register(model)
