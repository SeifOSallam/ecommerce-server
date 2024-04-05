from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.db.models import Q, Prefetch
from rest_framework.decorators import api_view,action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets,filters
from .serializer import RateSerializer
from .models import Rate
from products.models import Product
from user.models import User

class RateViewSet(viewsets.ModelViewSet):
    serializer_class = RateSerializer
    queryset = Rate.objects.all()
    
    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)

        
    # def get_queryset(self):
    #     queryset = super().get_queryset() 
    #     category = self.request.query_params.get('category')
    #     name = self.request.query_params.get('name')
       
    #     if category:
    #         queryset = queryset.filter(category__name=category)

    #     if name:
    #         queryset = queryset.filter(Q(name__icontains=name) | Q(description__icontains=name))
        
    #     queryset = queryset.prefetch_related(Prefetch('product_set', queryset=Product.objects.all(), to_attr='product'))
    #     return queryset
    
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     try:
    #         self.perform_destroy(instance)
    #     except:
    #         return Response({"detail": "Failed to delete the object."}, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({"detail": "Object deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

