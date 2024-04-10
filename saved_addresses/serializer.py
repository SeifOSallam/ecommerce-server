from rest_framework import serializers

from .models import SavedAddresses


class SavedAddressesSerializer(serializers.ModelSerializer):
    mobile_number = serializers.RegexField(
        "^01[0125][0-9]{8}$",
        allow_blank=False,
        required=True,
        error_messages={
            "invalid": "Number should be 11 digits and start with '01[0|1|2|5]'"
        },
    )

    class Meta:
        model = SavedAddresses
        fields = "__all__"
        read_only_fields = ["user"]
