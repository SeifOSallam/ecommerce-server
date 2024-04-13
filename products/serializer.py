from rest_framework import serializers

from rate.models import Rate
from review.serializer import ReviewSerializer

from .models import Image, Product


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(required=False)

    class Meta:
        model = Image
        fields = ("image_url",)


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    average_rate = serializers.SerializerMethodField(source="get_average_rate")
    total_rates = serializers.SerializerMethodField(source="get_total_rates")

    def get_total_rates(self, obj):
        rates = Rate.objects.filter(product=obj)

        total_rates = rates.count()

        return total_rates

    def get_average_rate(self, obj):
        rates = Rate.objects.filter(product=obj)

        total_rates = rates.count()
        sum_of_rates = sum(rate.rate for rate in rates)
        return sum_of_rates / total_rates if total_rates > 0 else 0

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "stock",
            "category",
            "images",
            "average_rate",
            "total_rates",
            "stripe_id",
        )
