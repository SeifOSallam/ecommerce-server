from rest_framework import serializers
from .models import Product, Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image_url',)

class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    # def validate(self, data):
    #     if data['price'] > 10:
    #         raise serializers.ValidationError("Price must be positive")
    #     return data

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock', 'category', 'images')