from django.shortcuts import render
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from rest_framework import status,viewsets,filters
from .serializer import SavedAddressesSerializer
from .models import SavedAddresses

class SavedAddressesViewSet(viewsets.ModelViewSet):
    serializer_class = SavedAddressesSerializer
    queryset = SavedAddresses.objects.all()

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)