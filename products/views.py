from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ProductSerializer
from .models import Product, Image
from django.http import Http404
from rest_framework import viewsets, filters
from django.db.models import Q, Prefetch, Count, Avg
from user.models import IsAdminOrReadOnly
from review.models import Review
from review.serializer import ReviewSerializer
from rest_framework.permissions import IsAuthenticated


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        name = self.request.query_params.get('name')
        rate_gt = self.request.query_params.get('rate_gt')
        rate_lt = self.request.query_params.get('rate_lt')
        price_gt = self.request.query_params.get('price_gt')
        price_lt = self.request.query_params.get('price_lt')

        # product/?rate_gt=1&rate_lt=4
        if rate_gt:
            queryset = queryset.annotate(avg_rate=Avg(
                'rate__rate')).filter(avg_rate__gt=float(rate_gt))

        if rate_lt:
            queryset = queryset.annotate(avg_rate=Avg(
                'rate__rate')).filter(avg_rate__lt=float(rate_lt))

        # product/?price_gt=1&price_lt=4
        if price_gt:
            queryset = queryset.annotate(avg_price=Avg('price')).filter(
                avg_price__gt=float(price_gt))

        if price_lt:
            queryset = queryset.annotate(avg_price=Avg('price')).filter(
                avg_price__lt=float(price_lt))

        if category:
            queryset = queryset.filter(category__name=category)

        if name:
            queryset = queryset.filter(
                Q(name__icontains=name) | Q(description__icontains=name))

        queryset = queryset.prefetch_related(
            Prefetch('image_set', queryset=Image.objects.all(), to_attr='images'))
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Retrieve reviews associated with the product
        reviews = Review.objects.filter(product=instance)
        review_serializer = ReviewSerializer(reviews, many=True)

        # Add reviews to the response data
        data = serializer.data
        data['reviews'] = review_serializer.data

        return Response(data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except:
            return Response({"detail": "Failed to delete the object."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Object deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    def get_permissions(self):
        if self.action in ['add_review']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminOrReadOnly]  
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        product = self.get_object()
        request.data['product'] = product.id
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def popular_products(self, request):
        queryset = self.get_queryset().annotate(
            total_rates=Count('rate')).order_by('-total_rates')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# POST /api/cart/: Add a product to the user's shopping cart.
# GET /api/cart/: Get the user's shopping cart.
# PUT /api/cart/<product_id>/: Update the quantity of a product in the user's shopping cart.
# DELETE /api/cart/<product_id>/: Remove a product from the user's shopping cart.
# POST /api/cart/checkout/: Checkout the user's shopping cart.