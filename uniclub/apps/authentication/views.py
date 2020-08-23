from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
)
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.core.views import PublicAPIMixin
from apps.sms.services import send_otp

from .serializers import (
    TokenObtainPairSerializer, RegisterAccountSerializer, VerifyOTPSerializer
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
        return Response(status=status.HTTP_200_OK)


class RegisterResendOTPView():
    pass
