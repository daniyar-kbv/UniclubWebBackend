from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)
from rest_framework_simplejwt.serializers import PasswordField
from phonenumber_field.serializerfields import PhoneNumberField

from apps.sms.services import verify_otp

User = get_user_model()


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    username_field = "username"

    def validate(self, attrs):
        try:
            attrs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**attrs)
        if self.user is None or not self.user.is_active:
            raise AuthenticationFailed(
                self.error_messages["no_active_account"], "no_active_account",
            )
        refresh = self.get_token(self.user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["veredis"] = "voyager-1"
        token["type"] = user.user_type

        return token


class TokenOutputSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class RegisterAccountSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True)
    mobile_phone = PhoneNumberField(
        required=True, write_only=True, label="Мобильный номер"
    )

    class Meta:
        model = User
        fields = (
            "mobile_phone",
            "password"
        )

    def validate(self, attrs):
        if User.objects.filter(is_active=True, mobile_phone=attrs.get("mobile_phone")).exists():
            raise serializers.ValidationError("user is already registered")
        return super().validate(attrs)

    def create(self, validated_data):
        user, created = User.objects.get_or_create(**validated_data)
        return user


class VerifyOTPSerializer(serializers.Serializer):
    code = serializers.CharField(label="OTP код")
    mobile_phone = PhoneNumberField(label="Номер телефона", required=False)

    def validate(self, attrs):
        verify_otp(code=attrs["code"], mobile_phone=attrs["mobile_phone"], save=True)
        return attrs
