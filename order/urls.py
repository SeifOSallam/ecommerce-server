from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("", views.OrderViewSet)
router.register("item/orderitem", views.OrderItemViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<pk>/cancel",
        views.OrderViewSet.as_view({"post": "cancel_order"}),
        name="cancel_order",
    ),
]
