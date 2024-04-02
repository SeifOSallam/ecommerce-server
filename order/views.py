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


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    


