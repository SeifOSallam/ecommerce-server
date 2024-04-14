from datetime import datetime, timedelta

from django.db.models import Prefetch, Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from cart.models import CartItem
from products.serializer import ProductSerializer

from .models import Order, OrderItem, Product
from .serializer import OrderItemSerializer, OrderSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination
    page_size = 5
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        user = self.request.query_params.get("user")

        if user:
            queryset = queryset.filter(Q(user=user))

        queryset = queryset.prefetch_related(
            Prefetch("orderitem_set",
                     queryset=OrderItem.objects.all(), to_attr="items")
        )

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_items = CartItem.objects.filter(user=request.user)

        if len(cart_items) == 0:
            return Response(
                {"message": "Cart is Empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        total_price = 0
        for item in cart_items:
            total_price += item.product.price * item.quantity

        serializer.validated_data["total_price"] = total_price
        serializer.validated_data["delivery_date"] = datetime.now(
        ) + timedelta(days=3)
        serializer.validated_data["user"] = request.user

        order = serializer.save()

        for item in cart_items:
            OrderItem.objects.create(
                product=item.product, order=order, quantity=item.quantity
            )
            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        if order.status == "DELIVERED" or order.status == "CANCELED":
            return Response(
                {"message": "Order cannot be canceled"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = "CANCELED"
        order.save()
        return Response({"message": "Order cancelled successfully"})


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
            product = Product.objects.get(pk=orderitem_data["product"])
            product_serializer = ProductSerializer(product)
            orderitem_data["product"] = product_serializer.data

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        product = Product.objects.get(pk=instance.product_id)
        product_serializer = ProductSerializer(product)
        data = serializer.data
        data["product"] = product_serializer.data

        return Response(data)
