from rest_framework import serializers

from .models import OTP


class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ("code",)
