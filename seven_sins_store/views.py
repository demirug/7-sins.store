from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render


def info(request: WSGIRequest):
    return render(request, 'info.html')