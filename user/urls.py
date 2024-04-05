from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import MeView, UserViewSet, VerifyEmail

router = DefaultRouter()
router.register("", UserViewSet, basename="user")

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
]
