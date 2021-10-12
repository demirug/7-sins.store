from django.shortcuts import render
from django.views.generic import DetailView, ListView

__all__ = ('ProductDetailView', 'ProductListView')

from products.models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    ordering = ['pk']

    def get_queryset(self):
        return Product.objects.filter(active=True).order_by(*self.ordering)
