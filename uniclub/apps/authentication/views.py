from django.db import transaction
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
)
from rest_framework.generics import CreateAPIView

from apps.core.views import PublicAPIMixin
from apps.sms.services import send_otp

from .serializers import TokenObtainPairSerializer, RegisterAccountSerializer


class TokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class RegisterAccountView(PublicAPIMixin, CreateAPIView):
    serializer_class = RegisterAccountSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        mobile_phone = serializer.validated_data["mobile_phone"]
        serializer.save()
        transaction.on_commit(lambda: send_otp(mobile_phone))


class VerifyAccountView():
    pass


class RegisterResendOTPView():
    pass
