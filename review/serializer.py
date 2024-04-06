from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    profile_image = serializers.SerializerMethodField(read_only=True)
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    def get_profile_image(self, obj):
        return obj.user.profile_image.url if obj.user.profile_image else None
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'content','full_name','profile_image']
        read_only_fields = ['user']  
