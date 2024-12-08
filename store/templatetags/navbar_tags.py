from django import template
from store.models import Category

register = template.Library()


@register.inclusion_tag('navbar.html')
def navbar_categories(request):
    # Get the cart data from the session
    cart = request.session.get('cart', {})  # Assuming the cart is stored in the session as a dictionary

    # Get all categories from the database
    categories = Category.objects.all()

    # Return both categories and cart
    return {'categories': categories, 'cart': cart}
