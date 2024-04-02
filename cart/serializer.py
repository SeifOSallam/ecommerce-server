from rest_framework import serializers
from .models import Cart, CartItem
from products.serializer import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('cart', 'quantity', 'product')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['items'] = CartItemSerializer(instance.items.all(), many=True).data
        return representation

