from rest_framework import serializers

from products.serializer import ProductSerializer

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ("id", "product", "order", "quantity")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_data = instance.product
        product_serializer = ProductSerializer(product_data)
        representation["product"] = product_serializer.data
        return representation


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "starting_date",
            "delivery_date",
            "total_price",
            "status",
            "user",
            "items",
            "address",
            "address_name",
            "address_mobile",
            "address_desc",
        )
        read_only_fields = ["user"]
