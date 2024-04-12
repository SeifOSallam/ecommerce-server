from django.shortcuts import render
from django.http import Http404
from django.http.response import HttpResponse, JsonResponse
from django.db.models import Q, Prefetch
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from .serializer import CartItemSerializer
from .models import CartItem, Product
from products.serializer import ProductSerializer
from user.models import User
from rest_framework.generics import ListAPIView


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        return super().perform_create(serializer)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        for cartitem_data in serializer.data:
            product = Product.objects.get(
                pk=cartitem_data['product'].get('id'))
            product_serializer = ProductSerializer(product)
            cartitem_data['product'] = product_serializer.data

        return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        user = self.request.user
        queryset = self.queryset.filter(user=user)
        queryset.delete()
        return Response({"message": "Cart Cleared"})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        product = Product.objects.get(pk=instance.product_id)
        product_serializer = ProductSerializer(product)
        data = serializer.data
        data['product'] = product_serializer.data

        return Response(data)
