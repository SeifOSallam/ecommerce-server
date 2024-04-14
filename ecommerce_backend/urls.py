from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("user.urls")),
    path("product/", include("products.urls")),
    path("category/", include("category.urls")),
    path("rate/", include("rate.urls")),
    path("cart/", include("cart.urls")),
    path("order/", include("order.urls")),
    path("review/", include("review.urls")),
    path("address/", include("saved_addresses.urls")),
    path("wish_list/", include("wish_list.urls")),
    path("checkout/", include("payment.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/schema/", SpectacularAPIView.as_view(), name="api_schema"),
    path(
        "",
        SpectacularRedocView.as_view(url_name="api_schema"),
        name="api_docs",
    ),
]
