from django import forms

from orders.models import Order
from products.models import Product


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'status']
