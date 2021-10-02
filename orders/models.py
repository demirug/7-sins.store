from django.db import models


class OrderItem(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    count = models.PositiveIntegerField()


class Order(models.Model):
    orderItems = models.ManyToManyField(OrderItem)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)