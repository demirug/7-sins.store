from django import forms

from orders.models import Order


class OrderModelForm(forms.ModelForm):
    full_name = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Адресс доставки', widget=forms.TextInput(attrs={'class': 'form-control'}))
    additional = forms.CharField(label='Коментарий', required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'email', 'address', 'additional']
