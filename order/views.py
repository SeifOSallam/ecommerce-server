from django.shortcuts import render
from rest_framework.response import Response
from .serializer import OrderSerializer, OrderItemSerializer
from rest_framework import viewsets, filters, status
from django.db.models import Q, Prefetch
from .models import Order, SavedAddresses, OrderItem, Product
from saved_addresses.serializer import SavedAddressesSerializer
from products.serializer import ProductSerializer
from rest_framework.decorators import action
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
url = os.getenv("FRONT_URL")


class StripeCheckoutView(APIView):
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1P4djx03YeN96iJ6kaJD768g',
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card'],
                mode='payment',
                success_url=url +
                '?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=url + '?canceled=true',
            )
            return redirect(checkout_session.url)
        except:
            return Response(
                {'error': 'Invalid Transaction'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        user = self.request.query_params.get('user')

        if user:
            queryset = queryset.filter(Q(user=user))

        queryset = queryset.prefetch_related(
            Prefetch('orderitem_set', queryset=OrderItem.objects.all(), to_attr='items'))

        return queryset

    def perform_create(self, serializer):
        line_items = self.request.data['orderitem_data'].map(lambda item: {
            'price': item['product'].price,
            'quantity': item['quantity'],
        })
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items,
                payment_method_types=['card'],
                mode='payment',
                success_url=url +
                '?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=url + '?canceled=true',
            )
            serializer.save(user=self.request.user)
            return redirect(checkout_session.url)
        except:
            return Response(
                {'error': 'Invalid Transaction'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        for order_data in serializer.data:
            saved_address = SavedAddresses.objects.get(
                pk=order_data['saved_address'])
            saved_address_serializer = SavedAddressesSerializer(saved_address)
            order_data['saved_address'] = saved_address_serializer.data

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        saved_address = SavedAddresses.objects.get(
            pk=instance.saved_address_id)
        saved_address_serializer = SavedAddressesSerializer(saved_address)
        data = serializer.data
        data['saved_address'] = saved_address_serializer.data

        return Response(data)

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        if (order.status == "DELIVERED" or order.status == "CANCELED"):
            return Response({'message': 'Order cannot be canceled'},
                            status=status.HTTP_400_BAD_REQUEST)

        order.status = 'CANCELED'
        order.save()
        return Response({'message': 'Order cancelled successfully'})


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
