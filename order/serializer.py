from rest_framework import serializers
from .models import Order
from cart.serializer import CartSerializer
from saved_addresses.serializer import SavedAddressesSerializer

class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    saved_address = SavedAddressesSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'date', 'total_price', 'status', 'cart','user','saved_address')
        