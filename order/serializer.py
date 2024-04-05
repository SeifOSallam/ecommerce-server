from rest_framework import serializers

from cart.serializer import CartSerializer
from saved_addresses.serializer import SavedAddressesSerializer

from .models import Cart, Order, SavedAddresses, User


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            "id",
            "date",
            "total_price",
            "status",
            "user",
            "saved_address",
        )
        read_only_fields = ["user"]
