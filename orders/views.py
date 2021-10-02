from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect

from orders.cart import Cart

__all__ = ('cart', 'add_Product', 'updateCart', 'remove_Product', 'confirm', 'track')

from orders.models import OrderItem, Order

from products.models import Product


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
    ids = [k[4:] for k in request.POST.keys() if str(k).startswith('PK__')]
    for product in Product.objects.filter(pk__in=ids):
        cart.set(product, int(request.POST['PK__' + str(product.pk)]), save=False)
    cart.save()
    return redirect('cart')


def track(request, pk):
    return render(request, 'orders/track.html', context={'order': Order.objects.filter(pk=pk).first()})
