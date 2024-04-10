from rest_framework import serializers
from .models import WishList
from products.serializer import ProductSerializer
from products.models import Product


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ('id', 'customer', 'product')
        read_only_fields = ['customer']

    # def perform_create(self, serializer):
    #     serializer.save(customer=self.request.user)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = ProductSerializer(instance.product).data
        return representation