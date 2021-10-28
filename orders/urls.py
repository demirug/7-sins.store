from django.urls import path

from orders.views import *

urlpatterns = [
    path('add/<int:pk>', add_Product, name='add'),
    path('remove/<int:pk>', remove_Product, name='remove'),
    path('update/', updateCart, name='update'),
    path('confirm/', confirm, name='confirm'),
    path('track/<int:pk>', TrackView.as_view(), name='track'),
]
