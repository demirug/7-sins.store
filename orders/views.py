from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from orders.forms import OrderModelForm
from orders.models import OrderItem, Order
from orders.cart import Cart
from products.models import Product

__all__ = ('cart', 'add_Product', 'updateCart', 'remove_Product', 'confirm', 'TrackView')


def confirm(request):
    cart = Cart(request)

    if not cart.cart_items:
        return redirect('cart')

    cart.updateQuantity()
    products = Product.objects.filter(pk__in=cart.cart_items.keys())
    totalPrice = sum([cart.cart_items[str(product.pk)] * product.price for product in products])

    form = OrderModelForm(request.POST or None)

    if form.is_valid():
        order = form.save()
        for product in products:
            item = OrderItem()
            item.product = product
            item.count = cart.cart_items[str(product.pk)]
            item.save()
            order.orderItems.add(item)
        order.price = totalPrice
        order.save()
        order.sendEmail(order.StatusChoice.NEW)
        cart.clear()
        return render(request, 'orders/accepted.html', context={'pk': order.pk})
    else:

        for tag in form.errors.as_data():
            for validationError in form.errors.as_data()[tag]:
                for error in validationError:
                    messages.error(request, error)

        return render(request, 'orders/confirm.html', context={
            'form': form,
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
    product = Product.objects.filter(pk=pk).first()
    if product:
        if product.quantity == 0:
            messages.error(request, 'Данного товара нет в наличии')
            return redirect('view', product.slug)
        else:
            Cart(request).add(product, 1)
            return redirect('cart')
    else:
        return HttpResponseBadRequest('Error: Incorrect PK transmitted')


def remove_Product(request, pk):
    product = Product.objects.filter(pk=pk).first()
    if product:
        Cart(request).set(product, 0)
        return redirect('cart')
    else:
        return HttpResponseBadRequest('Error: Incorrect PK transmitted')


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
