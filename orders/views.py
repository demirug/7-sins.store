from django.shortcuts import render, redirect

from orders.cart import Cart

__all__ = ('cart', 'add_Product', 'updateCart')

from products.models import Product


def cart(request):
    cart = Cart(request)

    products = Product.objects.filter(pk__in=cart.cart_items.keys())

    return render(request, 'orders/cart.html', context={
        'cart': cart.cart_items,
        'products': {product: cart.cart_items[str(product.pk)] for product in products},
        'totalPrice': sum([cart.cart_items[str(product.pk)] * product.price for product in products])})


def add_Product(request, pk):
    product = Product.objects.get(pk=pk)
    Cart(request).add(product, 1)
    return redirect('cart')


def updateCart(request):
    cart = Cart(request)
    ids = [int(k[4:]) for k in request.POST.keys() if str(k).startswith('PK__')]
    for product in Product.objects.filter(pk__in=ids):
        cart.set(product, int(request.POST['PK__' + str(product.pk)]), save=False)
    cart.save()
    return redirect('cart')
