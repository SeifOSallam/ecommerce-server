from django.shortcuts import render
from django.http import Http404
from django.http.response import HttpResponse, JsonResponse
from django.db.models import Q, Prefetch
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets,filters
from .serializer import WishListSerializer
from products.models import Product
from .models import WishList
from products.serializer import ProductSerializer

class WishViewSet(viewsets.ModelViewSet):
    serializer_class = WishListSerializer
    queryset = WishList.objects.all()
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(customer=self.request.user)