import os

import stripe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartItem

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
front_url = os.getenv("FRONT_URL")
# Create your views here.


class StripeCheckoutView(APIView):
    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)

        if len(cart_items) == 0:
            return Response(
                {"message": "Cart is Empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        line_items = [
            {"price": item.product.stripe_id, "quantity": item.quantity}
            for item in cart_items
        ]
        print(line_items)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                payment_method_types=["card"],
                mode="payment",
                success_url=front_url
                + "orders/"
                + "?success=true&session_id={CHECKOUT_SESSION_ID}",
                cancel_url=front_url + "orders/" + "?canceled=true",
            )
            # serializer.save(user=self.request.user)
            return Response(
                {"redirect_url": checkout_session.url}, status=status.HTTP_200_OK
            )
        except stripe.error.StripeError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": f"e is {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
