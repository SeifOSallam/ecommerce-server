from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import MeView, UserViewSet, VerifyEmail, SendPasswordResetEmail, ResetPassword, SendEmailVerification

router = DefaultRouter()
router.register("", UserViewSet, basename="user")

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("verify-email/", VerifyEmail.as_view(), name="verify-email"),
    path("send-reset-password/", SendPasswordResetEmail.as_view(), name="send-reset-password"),
    path("reset-password/", ResetPassword.as_view(), name="reset-password"),
    path("send-verify-email/", SendEmailVerification.as_view(), name="send-verify-email"),
    path("", include(router.urls)),  # Must be at last
]
