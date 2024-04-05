from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import CategorySerializer
from .models import Category
from django.http import Http404
from rest_framework import viewsets,filters
from django.db.models import Q, Prefetch
from user.models import IsAdminOrReadOnly

class  CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset() 
        name = self.request.query_params.get('name')
        
        if name:
            queryset = queryset.filter(Q(name__icontains=name))
    
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except:
            return Response({"detail": "Failed to delete the object."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Object deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
   
# GET /api/categories/: Get a list of all product categories.
# GET /api/categories/<category_id>/products/: Get a list of products in a specific category.
