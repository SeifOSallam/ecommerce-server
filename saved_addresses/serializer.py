from rest_framework import serializers
from .models import SavedAddresses

class SavedAddressesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedAddresses
        fields ="__all__"
        read_only_fields = ['user']
