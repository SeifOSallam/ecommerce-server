from rest_framework import serializers
from .models import Cart, CartItem
from products.serializer import ProductSerializer
from products.models import Image
from products.serializer import ImageSerializer

class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'quantity', 'product')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_data = instance.product
        product_serializer = ProductSerializer(product_data).data
        image = Image.objects.filter(product=product_data.pk).first()
        representation['image'] = ImageSerializer(image).data if image else None
        representation['product'] = product_serializer
        return representation


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items')
        read_only_fields = ['user']  
    
    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['items'] = CartItemSerializer(instance.items.all(), many=True).data
        return representation

