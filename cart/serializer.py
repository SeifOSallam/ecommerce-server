from rest_framework import serializers
from .models import  CartItem
from products.serializer import ProductSerializer
from products.models import Image
from products.serializer import ImageSerializer

class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('id', 'quantity', 'product')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_data = instance.product
        product_serializer = ProductSerializer(product_data).data
        image = Image.objects.filter(product=product_data.pk).first()
        representation['image'] = ImageSerializer(image).data if image else None
        representation['product'] = product_serializer
        return representation
    
