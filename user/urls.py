from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import SignUp

urlpatterns = [
    path("register/", SignUp.as_view(), name="sign_up"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
]
