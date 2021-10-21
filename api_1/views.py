from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.mixins import ListModelMixin

from api_1.serializers import OrderSerializer
from orders.models import Order


class OrderListView(ListModelMixin, GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderEmailListView(ListModelMixin, GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'email'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderView(RetrieveUpdateAPIView, RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
