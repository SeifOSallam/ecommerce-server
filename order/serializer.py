from rest_framework import serializers
from .models import Order, OrderItem
from cart.serializer import CartSerializer
from saved_addresses.serializer import SavedAddressesSerializer

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'order', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'date', 'total_price', 'status', 'user', 'saved_address', 'items')
        read_only_fields = ['user']  
       