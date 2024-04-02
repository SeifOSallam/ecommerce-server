from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from .serializers import SignUpSerializer


class SignUp(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SignUpSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()
