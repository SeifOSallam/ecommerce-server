from django.shortcuts import render
from django.http import Http404
from django.http.response import HttpResponse, JsonResponse
from django.db.models import Q, Prefetch
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets,filters
from .serializer import CartSerializer,CartItemSerializer
from .models import Cart,CartItem

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset() 
        
        # queryset = queryset.prefetch_related(Prefetch('cartitem_set', queryset=CartItem.objects.all(), to_attr='items'))
        return queryset