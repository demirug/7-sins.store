from django.urls import path, include

from api_1.views import *

urlpatterns = [
    path('orders/<int:pk>/', OrderView.as_view()),
    path('orders/<str:email>/', OrderEmailListView.as_view()),
    path('orders/', OrderListView.as_view()),
]