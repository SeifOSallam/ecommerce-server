import jwt
import os
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny

from .models import User
from .permissions import CreateOnly, IsOwner
from .serializers import EmailVerificationSerializer, UserSerializer
from .utils import Util
from dotenv import load_dotenv

load_dotenv()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [IsOwner]

    def get_permissions(self):
        if self.action == "create":
            return [CreateOnly()]
        return super().get_permissions()

    @extend_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)

    def create(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data

        # getting tokens
        userId = User.objects.get(id=user["id"])
        accessToken = RefreshToken.for_user(userId).access_token
        refreshToken = RefreshToken.for_user(userId)
        # send email for user verification
        absurl = f"{os.getenv('FRONT_URL')}/verify-email/{accessToken}"
        email_body = (
            "Hi "
            + user["username"]
            + " Use the link below to verify your email \n"
            + absurl
        )
        data = {
            "email_body": email_body,
            "to_email": user["email"],
            "email_subject": "Verify your email",
        }

        Util.send_email(data=data)

        return Response(
            {"access_token": str(accessToken),
             "refresh_token": str(refreshToken)},
            status=status.HTTP_201_CREATED,
        )


class MeView(APIView):
    """
    Retrieve logged in user data
    """

    @extend_schema(responses={200: UserSerializer})
    def get(self, request):
        serialzier = UserSerializer(request.user)
        return Response(serialzier.data, status=status.HTTP_200_OK)


class SendEmailVerification(GenericAPIView):
    """
    Send email verification link to user's email
    """

    def post(self, request):
        user = request.user
        print(user)
        if user.is_verified:
            return Response(
                {"error": "Email is already verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = jwt.encode(
            {"user_id": user.pk}, os.getenv("SECRET_KEY"), algorithm="HS256"
        )
        absurl = f"{os.getenv('FRONT_URL')}/verify-email/{token}"
        email_body = (
            "Hello, \n Use link below to verify your email \n"
            + absurl
        )
        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Verify your email",
        }
        Util.send_email(data)
        return Response(
            {"success": "We have sent you a link to verify your email"},
            status=status.HTTP_200_OK,
        )


class VerifyEmail(GenericAPIView):
    """
    Verify user's email.
    Intended to be used through link sent to your regeistered email
    """

    serializer_class = EmailVerificationSerializer

    def post(self, request):
        token = request.data.get("token")
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            print(payload)
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {"email": "Successfully activated"}, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class SendPasswordResetEmail(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.filter(email=email).first()
        if user:
            token = jwt.encode(
                {"user_id": user.pk}, os.getenv("SECRET_KEY"), algorithm="HS256"
            )
            relative_link = "reset-password"
            absurl = f"{os.getenv('FRONT_URL')}/{relative_link}/{token}"
            email_body = (
                "Hello, \n Use link below to reset your password \n"
                + absurl
            )
            data = {
                "email_body": email_body,
                "to_email": email,
                "email_subject": "Reset your password",
            }
            Util.send_email(data)
            return Response(
                {"success": "We have sent you a link to reset your password"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "No user with this email"}, status=status.HTTP_400_BAD_REQUEST
        )


class ResetPassword(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        password = request.data.get("password")
        if not token or not password:
            return Response(
                {"error": "Token and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            payload = jwt.decode(token, os.getenv(
                "SECRET_KEY"), algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            user.set_password(password)
            user.save()
            return Response(
                {"success": "Password reset success"},
                status=status.HTTP_200_OK,
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Token expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError, jwt.exceptions.InvalidTokenError):
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )
