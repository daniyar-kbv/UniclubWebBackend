from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema

from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
)
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from apps.users.views import ClientAPIMixin
from apps.core.views import PublicAPIMixin
from apps.sms.services import send_otp

from .serializers import (
    TokenObtainPairSerializer, RegisterAccountSerializer, VerifyOTPSerializer, UpdatePasswordSerializer
)

User = get_user_model()


class TokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class RegisterAccountView(PublicAPIMixin, CreateAPIView):
    """
    Регистрация клиента
    """

    serializer_class = RegisterAccountSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        mobile_phone = serializer.validated_data["mobile_phone"]
        serializer.save()
        transaction.on_commit(lambda: send_otp(mobile_phone))


class VerifyAccountView(PublicAPIMixin, GenericAPIView):
    """
    Верификация OTP кода для завершения регистрации
    """

    queryset = User.objects.filter(is_active=False)
    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(self.queryset, mobile_phone=serializer.validated_data["mobile_phone"])
        user.is_active = True
        user.save(update_fields=["is_active"])

        refresh = TokenObtainPairSerializer.get_token(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response(data)


class RegisterResendOTPView():
    pass


class UpdatePasswordView(ClientAPIMixin, APIView):
    @swagger_auto_schema(
        request_body=UpdatePasswordSerializer,
        responses={200: UpdatePasswordSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = UpdatePasswordSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')
        user = request.user
        user.set_password(password)
        user.save()
        return Response(serializer.data)
