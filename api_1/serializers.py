from rest_framework import serializers

from orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    #productID = serializers.IntegerField(source='product.pk')
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = OrderItem
        exclude = ['id']


class OrderSerializer(serializers.ModelSerializer):

    orderItems = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        return instance

