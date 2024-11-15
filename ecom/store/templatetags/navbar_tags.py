from django import template
from store.models import Category




register = template.Library()


@register.inclusion_tag('navbar.html')
def navbar_categories():
    categories = Category.objects.all()
    return {'categories': categories}

