from django.urls import path

from .views import StripeCheckoutView

urlpatterns = [path("", StripeCheckoutView.as_view(), name="checkout")]
