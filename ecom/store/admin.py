from django.contrib import admin
from .models import Category, Customer, Product, Order
from django.contrib.auth.models import Group


models = [Category, Customer, Product, Order]

for model in models:
    admin.site.register(model)

admin.site.unregister(Group)
