from rest_framework import serializers
from .models import WishList
from products.serializer import ProductSerializer
from products.models import Product
from products.serializer import ProductSerializer
from products.models import Image
from products.serializer import ImageSerializer

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ('id', 'customer', 'product')
        read_only_fields = ['customer']

    # def perform_create(self, serializer):
    #     serializer.save(customer=self.request.user)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_data = instance.product
        image = Image.objects.filter(product=product_data.pk).first()
        representation['image'] = ImageSerializer(image).data.get('image_url') if image else None
        representation['product'] = ProductSerializer(instance.product).data
        return representation
    