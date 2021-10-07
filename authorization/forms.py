from django import forms
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    login = forms.CharField(label='Логин', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        login = self.cleaned_data.get('login')
        password = self.cleaned_data.get('password')
        user = authenticate(username=login, password=password)
        if not user:
            raise forms.ValidationError('Некорректный логин или пароль')
        return super().clean(*args, **kwargs)