from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView

__all__ = ('ProductDetailView', 'ProductListView')

from products.models import Product


def ProductDetailView(request, slug, pk):
    product = get_object_or_404(Product, pk=pk)
    if slug != product.slug:
        return redirect(product.get_absolute_url())
    print(product.price)
    return render(request, 'products/detail.html', context={'object': product})


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    ordering = ['pk']

    def get_queryset(self):
        return Product.objects.filter(active=True).order_by(*self.ordering)
