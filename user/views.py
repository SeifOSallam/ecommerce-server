import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import CreateOnly, IsOwner
from .serializers import EmailVerificationSerializer, UserSerializer
from .utils import Util


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]

    def get_permissions(self):
        if self.action == "create":
            return [CreateOnly()]
        return super().get_permissions()

    @extend_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data

        # getting tokens
        userId = User.objects.get(id=user["id"])
        accessToken = RefreshToken.for_user(userId).access_token
        refreshToken = RefreshToken.for_user(userId)
        # send email for user verification
        current_site = get_current_site(request).domain
        relative_link = reverse("email-verify")
        absurl = "http://" + current_site + relative_link + "?token=" + str(accessToken)
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
            {"access_token": str(accessToken), "refresh_token": str(refreshToken)},
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


class VerifyEmail(GenericAPIView):
    """
    Verify user's email.
    Intended to be used through link sent to your regeistered email
    """

    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get("token")
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
