from django.shortcuts import render
from django.http import Http404
from django.http.response import HttpResponse, JsonResponse
from django.db.models import Q, Prefetch
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets,filters
from .serializer import CartSerializer,CartItemSerializer
from .models import Cart,CartItem,Product
from products.serializer import ProductSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        for cartitem_data in serializer.data:
            product = Product.objects.get(pk=cartitem_data['product'])
            product_serializer = ProductSerializer(product)
            cartitem_data['product'] = product_serializer.data

        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        product = Product.objects.get(pk=instance.product_id)
        product_serializer = ProductSerializer(product)
        data = serializer.data
        data['product'] = product_serializer.data

        return Response(data)

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    
    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)

        return queryset
    