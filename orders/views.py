from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from orders.models import OrderItem, Order
from orders.cart import Cart
from products.models import Product

__all__ = ('cart', 'add_Product', 'updateCart', 'remove_Product', 'confirm')

def confirm(request):
    cart = Cart(request)

    if not cart.cart_items:
        return redirect('cart')

    cart.updateQuantity()
    products = Product.objects.filter(pk__in=cart.cart_items.keys())
    totalPrice = sum([cart.cart_items[str(product.pk)] * product.price for product in products])

    if request.method == "POST":
        if request.POST['full_name'] and request.POST['email'] and request.POST['phone'] and request.POST['address']:
            order = Order()
            order.price = totalPrice
            order.full_name = request.POST['full_name']
            order.email = request.POST['email']
            order.phone = request.POST['phone']
            order.address = request.POST['address']

            # Order has double save to init PK for ManyToMany field
            order.save()

            for product in products:
                item = OrderItem()
                item.product = product
                item.count = cart.cart_items[str(product.pk)]
                item.save()
                order.orderItems.add(item)
            order.save()
            order.sendEmail(order.StatusChoice.NEW)
            cart.clear()
            return render(request, 'orders/accepted.html', context={'pk': order.pk})
        else:
            return HttpResponseBadRequest('Incorrect POST data')
    else:
        return render(request, 'orders/confirm.html', context={
            'cart': cart.cart_items,
            'products': {product: cart.cart_items[str(product.pk)] for product in products},
            'totalPrice': totalPrice
        })


def cart(request):
    cart = Cart(request)
    cart.updateQuantity()

    products = Product.objects.filter(pk__in=cart.cart_items.keys())
    return render(request, 'orders/cart.html', context={
        'cart': cart.cart_items,
        'products': {product: cart.cart_items[str(product.pk)] for product in products},
        'totalPrice': sum([cart.cart_items[str(product.pk)] * product.price for product in products])
    })


def add_Product(request, pk):
    product = Product.objects.get(pk=pk)
    Cart(request).add(product, 1)
    return redirect('cart')


def remove_Product(request, pk):
    product = Product.objects.get(pk=pk)
    Cart(request).set(product, 0)
    return redirect('cart')


def updateCart(request):
    cart = Cart(request)
    if request.POST['pk'] and request.POST['quantity']:
        cart.set_byID(request.POST['pk'], int(request.POST['quantity']))
        return HttpResponse('OK')
    else:
        return HttpResponseBadRequest('Incorrect POST data')


class TrackView(DetailView):
    model = Order
    template_name = 'orders/track.html'
