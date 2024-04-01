from rest_framework import serializers
from .models import Product, Image
from rate.models import Rate

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image_url',)

class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    

    average_rate = serializers.SerializerMethodField()
    total_rates = serializers.SerializerMethodField()
    
    def get_total_rates(self, obj): 
        rates = Rate.objects.filter(product=obj)
        
        total_rates = rates.count()
        
        return total_rates
    
    def get_average_rate(self, obj):
        rates = Rate.objects.filter(product=obj)
        
        total_rates = rates.count()
        sum_of_rates = sum(rate.rate for rate in rates)

        if total_rates > 0:
            average_rate = sum_of_rates / total_rates
        else:
            average_rate = 0
        
        return average_rate

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock', 'category', 'images', 'average_rate', 'total_rates')
