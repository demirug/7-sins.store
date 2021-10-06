from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from manager.forms import ProductModelForm, OrderModelForm
from orders.models import Order
from products.models import Product

__all__ = ('ProductListView', 'OrderListView', 'editProduct', 'createProduct', 'changeOrder')


class ProductListView(ListView):
    model = Product
    template_name = 'manager/productsList.html'
    ordering = ['pk']
    paginate_by = 10


class OrderListView(ListView):
    model = Order
    template_name = 'manager/ordersList.html'
    ordering = ['-pk']
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.annotate(
            custom_order=models.Case(
                models.When(status="NEW", then=1),
                models.When(status="ACCEPTED", then=2),
                models.When(status="CANCELED", then=4),
                models.When(status="DONE", then=3),
                output_field=models.IntegerField())
        ).order_by('custom_order')


def changeOrder(request, pk):
    form = OrderModelForm(data=request.POST or None, instance=get_object_or_404(Order, pk=pk))
    if form.is_valid():
        form.save()
        return redirect('manager:home')
    else:
        return render(request, 'manager/form.html', {'form': form, 'title': 'Редактирование заказа'})


def createProduct(request):
    form = ProductModelForm(data=request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('manager:home')
    else:
        return render(request, 'manager/form.html', {'form': form, 'title': 'Создание товара'})


def editProduct(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductModelForm(data=request.POST or None, files=request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('manager:home')
    else:
        return render(request, 'manager/form.html', {'form': form, 'title': 'Редактирование товара'})
