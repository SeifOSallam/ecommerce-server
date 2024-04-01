from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from rest_framework.decorators import api_view,action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ProductSerializer
from .models import Product, Image
from django.http import Http404
from rest_framework import viewsets,filters
from django.db.models import Q, Prefetch

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset() 
        category = self.request.query_params.get('category')
        name = self.request.query_params.get('name')
       
        if category:
            queryset = queryset.filter(category__name=category)

        if name:
            queryset = queryset.filter(Q(name__icontains=name) | Q(description__icontains=name))
        
        queryset = queryset.prefetch_related(Prefetch('image_set', queryset=Image.objects.all(), to_attr='images'))
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except:
            return Response({"detail": "Failed to delete the object."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Object deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    ## http://127.0.0.1:8000/product/1/


# GET /api/products/: Get a list of all products.***
# GET /api/products/<product_id>/: Get details of a specific product.**
    
# GET /api/categories/: Get a list of all product categories.***
# GET /api/categories/<category_id>/products/: Get a list of products in a specific category.***

# POST /api/cart/: Add a product to the user's shopping cart.
# GET /api/cart/: Get the user's shopping cart.
# PUT /api/cart/<product_id>/: Update the quantity of a product in the user's shopping cart.
# DELETE /api/cart/<product_id>/: Remove a product from the user's shopping cart.
# POST /api/cart/checkout/: Checkout the user's shopping cart.

