from django.core.handlers.wsgi import WSGIRequest

from products.models import Product


class Cart:
    def __init__(self, request: WSGIRequest):
        self.session = request.session
        # Product_ID, quantity
        cart_items = {}
        if self.session.get('CART'):
            cart_items = self.session['CART']
        self.cart_items = cart_items

    def add(self, product: Product, amount):
        key = str(product.pk)
        self.cart_items.setdefault(key, 0)
        self.cart_items[key] += amount

        if self.cart_items[key] > product.quantity:
            self.cart_items[key] = product.quantity
        self.save()

    def remove(self, product: Product, amount):
        key = str(product.pk)
        self.cart_items.setdefault(key, 0)
        self.cart_items[key] -= amount

        if self.cart_items[key] <= 0:
            del self.cart_items[key]
        self.save()

    def set(self, product: Product, amount, save=True):
        key = str(product.pk)
        self.cart_items.setdefault(key, 0)
        self.cart_items[key] = amount

        if self.cart_items[key] > product.quantity:
            self.cart_items[key] = product.quantity

        if self.cart_items[key] <= 0:
            del self.cart_items[key]

        if save:
            self.save()

    def updateQuantity(self):
        """
        Update quantity from database
        :return Products QuerySet
        """
        products = Product.objects.filter(pk__in=self.cart_items.keys())
        for product in products:
            self.set(product, self.cart_items[str(product.pk)], False)
        self.save()

    def clear(self):
        self.cart_items.clear()
        self.save()

    def save(self):
        self.session['CART'] = self.cart_items
        self.session.modified = True
