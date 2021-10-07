from django import template
from django.core.handlers.wsgi import WSGIRequest

from orders.cart import Cart

register = template.Library()


@register.simple_tag
def cart_size(request: WSGIRequest):
    return len(Cart(request).cart_items)
