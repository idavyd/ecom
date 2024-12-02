from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime as dt



class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=255)
    shipping_country = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return f' Shipping Address - {str(self.id)}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=255)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f'Order - {str(self.id)}'




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.BigIntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'


def create_s_address(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()


@receiver(pre_save,sender=Order)
def set_shipped_date_on_update(sender, instance: Order, **kwargs):
    if instance.pk:
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.is_shipped and not obj.is_shipped:
            instance.date_shipped = dt.datetime.now()


post_save.connect(create_s_address, sender=User)
