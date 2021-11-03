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
    TokenObtainPairSerializer, RegisterAccountSerializer, VerifyOTPSerializer, UpdatePasswordSerializer,
    RestorePasswordSerializer, RestorePasswordRequestSerializer
)
from .models import PasswordRestoreRequest

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


class RequestPasswordRestoreView(PublicAPIMixin, APIView):
    @swagger_auto_schema(
        request_body=RestorePasswordRequestSerializer,
        responses={200: RestorePasswordRequestSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = RestorePasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction.on_commit(lambda: send_otp(serializer.validated_data.get('mobile_phone')))
        return Response()


class VerifyRequestPasswordRestoreView(PublicAPIMixin, APIView):
    @swagger_auto_schema(
        request_body=VerifyOTPSerializer,
        responses={200: VerifyOTPSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(mobile_phone=serializer.validated_data.get('mobile_phone'))
        except:
            return Response('Пользователь не найден', status.HTTP_400_BAD_REQUEST)
        PasswordRestoreRequest.objects.create(user=user)
        return Response(serializer.data)


class PasswordRestoreView(PublicAPIMixin, APIView):
    @swagger_auto_schema(
        request_body=RestorePasswordSerializer,
        responses={200: RestorePasswordSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = RestorePasswordSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(mobile_phone=serializer.validated_data.get('mobile_phone'))
        except:
            return Response('Пользователь не найден', status.HTTP_400_BAD_REQUEST)
        restore_request = PasswordRestoreRequest.objects.active().filter(user=user).first()
        restore_request.is_used = True
        restore_request.save()
        password = serializer.validated_data.get('password')
        user.set_password(password)
        user.save()
        return Response(serializer.data)
