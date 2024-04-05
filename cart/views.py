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
    
    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)