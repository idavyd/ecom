from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem


models = [ShippingAddress, Order, OrderItem]
for model in models:
    admin.site.register(model)
