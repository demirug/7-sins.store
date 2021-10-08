from django import forms

from orders.models import Order
from products.models import Product


class ProductModelForm(forms.ModelForm):

    name = forms.CharField(label='Название товара', widget=forms.TextInput(attrs={'class': 'form-control'}))
    article = forms.CharField(label='Артикул', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    slug = forms.CharField(label='Slug', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.IntegerField(label='Цена', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(label='Доступное количество товара', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = '__all__'


class OrderModelForm(forms.ModelForm):

    full_name = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Адресс', widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(label='Статус', widget=forms.Select(attrs={'class': 'form-control'}), choices=Order.StatusChoice.choices)

    class Meta:
        model = Order
        fields = ['full_name', 'address', 'status']
