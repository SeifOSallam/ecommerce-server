from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.db.models import Q, Prefetch
from rest_framework.decorators import api_view,action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets,filters
from .serializer import ReviewSerializer
from .models import Review
from products.models import Product
from user.models import User
from rest_framework import permissions
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related(
            Prefetch(
                'user',
                queryset = User.objects.only('first_name', 'last_name', 'profile_image')
            )
        ).annotate(
            full_name = Concat(F('user__first_name'), Value(' '), F('user__last_name'), output_field=CharField())
        )
        return queryset
    
    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)
    
    
