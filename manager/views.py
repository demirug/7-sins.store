from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from manager.forms import ProductModelForm, OrderModelForm
from orders.models import Order
from products.models import Product

__all__ = ('ProductListView', 'OrderListView', 'editProduct', 'createProduct', 'changeOrder')


class ProductListView(LoginRequiredMixin, ListView):
    login_url = '/authorization/login/'
    model = Product
    template_name = 'manager/productsList.html'
    ordering = ['pk']
    paginate_by = 10


class OrderListView(LoginRequiredMixin, ListView):
    login_url = '/authorization/login/'
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
        ).order_by('custom_order', '-timestamp')


@login_required(login_url='/authorization/login/')
def changeOrder(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderModelForm(data=request.POST or None, instance=order)
    if form.is_valid():
        form.save()
        return redirect('manager:orders')
    else:
        return render(request, 'manager/orderForm.html', {'form': form, 'order': order})


@login_required(login_url='/authorization/login/')
def createProduct(request):
    form = ProductModelForm(data=request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('manager:products')
    else:
        return render(request, 'manager/productForm.html', {'form': form})


@login_required(login_url='/authorization/login/')
def editProduct(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductModelForm(data=request.POST or None, files=request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('manager:products')
    else:
        return render(request, 'manager/productForm.html', {'form': form})