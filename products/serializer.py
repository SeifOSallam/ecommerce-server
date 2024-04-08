from rest_framework import serializers
from .models import Product, Image
from rate.models import Rate
from category.models import Category
from review.serializer import ReviewSerializer
from category.serializer import CategorySerializer
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image_url']

class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    average_rate = serializers.SerializerMethodField(source='get_average_rate')
    total_rates = serializers.SerializerMethodField(source='get_total_rates')
    categoryName = serializers.SerializerMethodField(source='get_categoryName')

    def get_total_rates(self, obj): 
        rates = Rate.objects.filter(product=obj)
        return rates.count()
    
    def get_average_rate(self, obj):
        rates = Rate.objects.filter(product=obj)
        total_rates = rates.count()
        sum_of_rates = sum(rate.rate for rate in rates)
        return sum_of_rates / total_rates if total_rates > 0 else 0
    
    def get_categoryName(self, obj):
        category = Category.objects.get(pk=obj.category_id)
        return category.name
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        images = Image.objects.filter(product=instance)
        representation['images'] = ImageSerializer(images, many=True).data
        return representation
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'categoryName', 'average_rate', 'images', 'total_rates']