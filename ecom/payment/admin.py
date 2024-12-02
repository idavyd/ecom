from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User


models = [ShippingAddress, Order, OrderItem]
for model in models:
    admin.site.register(model)


# Create an OrderItem Inline
class OrderItemInLine(admin.StackedInline):
     model = OrderItem
     extra = 0


class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    inlines = [OrderItemInLine]


admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)






