from django.urls import path

from orders.views import *

urlpatterns = [
    path('add/<int:pk>', add_Product, name='add'),
    path('update', updateCart, name='update'),
]
