from rest_framework import serializers
from .models import Order, Cart, User, SavedAddresses
from cart.serializer import CartSerializer
from saved_addresses.serializer import SavedAddressesSerializer

class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ('id', 'date', 'total_price', 'status', 'cart', 'user', 'saved_address')
        read_only_fields = ['user']  
       