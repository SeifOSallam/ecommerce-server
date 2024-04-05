from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from rest_framework.decorators import api_view,action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import OrderSerializer
from .models import Order
from django.http import Http404
from rest_framework import viewsets,filters
from django.db.models import Q, Prefetch,Count,Avg
from .models import Order, Cart, User, SavedAddresses
from cart.serializer import CartSerializer
from saved_addresses.serializer import SavedAddressesSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        user = self.request.query_params.get('user')
        
        if user :
            queryset = queryset.filter(Q(user=user))
        
        return queryset
    
    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        for order_data in serializer.data:
            cart = Cart.objects.get(pk=order_data['cart'])
            saved_address = SavedAddresses.objects.get(pk=order_data['saved_address'])
            cart_serializer = CartSerializer(cart)
            saved_address_serializer = SavedAddressesSerializer(saved_address)
            order_data['cart'] = cart_serializer.data
            order_data['saved_address'] = saved_address_serializer.data

        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        cart = Cart.objects.get(pk=instance.cart_id)
        saved_address = SavedAddresses.objects.get(pk=instance.saved_address_id)
        cart_serializer = CartSerializer(cart)
        saved_address_serializer = SavedAddressesSerializer(saved_address)
        data = serializer.data
        data['cart'] = cart_serializer.data
        data['saved_address'] = saved_address_serializer.data

        return Response(data)

