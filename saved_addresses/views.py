from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import SavedAddresses
from .serializer import SavedAddressesSerializer


class SavedAddressesViewSet(viewsets.ModelViewSet):
    serializer_class = SavedAddressesSerializer
    queryset = SavedAddresses.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.user == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("You are not allowed to update this record.")

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("You are not allowed to delete this record.")
