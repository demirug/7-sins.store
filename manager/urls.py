from django.urls import path

from .views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('edit/<int:pk>', editProduct, name='edit'),
    path('create/', createProduct, name='create'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete'),
    path('order/<int:pk>', changeOrder, name='order'),
    path('feedback/', FeedbackListView.as_view(), name='feedback'),
    path('feedback/<int:pk>', answerFeedback, name='feedback_info'),
]
