from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

from authorization.forms import UserLoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next') or '/')
    else:
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            _login = form.cleaned_data.get('login')
            _password = form.cleaned_data.get('password')
            user = authenticate(username=_login, password=_password)
            login(request, user)
            return redirect(request.GET.get('next') or '/')
        else:
            return render(request, 'authorization/login.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')
