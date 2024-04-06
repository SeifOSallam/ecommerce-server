from django.shortcuts import render
from rest_framework.response import Response
from .serializer import OrderSerializer, OrderItemSerializer
from rest_framework import viewsets,filters
from django.db.models import Q, Prefetch
from .models import Order, SavedAddresses, OrderItem, Product
from saved_addresses.serializer import SavedAddressesSerializer
from products.serializer import ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        user = self.request.query_params.get('user')
        
        if user :
            queryset = queryset.filter(Q(user=user))
        
        queryset = queryset.prefetch_related(
            Prefetch('orderitem_set', queryset=OrderItem.objects.all(), to_attr='items'))

        return queryset
    
    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        for order_data in serializer.data:
            saved_address = SavedAddresses.objects.get(pk=order_data['saved_address'])
            saved_address_serializer = SavedAddressesSerializer(saved_address)
            order_data['saved_address'] = saved_address_serializer.data

        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        saved_address = SavedAddresses.objects.get(pk=instance.saved_address_id)
        saved_address_serializer = SavedAddressesSerializer(saved_address)
        data = serializer.data
        data['saved_address'] = saved_address_serializer.data

        return Response(data)

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        for orderitem_data in serializer.data:
            product = Product.objects.get(pk=orderitem_data['product'])
            product_serializer = ProductSerializer(product)
            orderitem_data['product'] = product_serializer.data

        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        product = Product.objects.get(pk=instance.product_id)
        product_serializer = ProductSerializer(product)
        data = serializer.data
        data['product'] = product_serializer.data

        return Response(data)