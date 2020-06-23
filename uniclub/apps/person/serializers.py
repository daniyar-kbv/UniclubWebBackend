from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Coach, ClientProfile, ClientChildren

User = get_user_model()


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        exclude = "club",


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = (
            "sex",
            "city",
            "birth_date",
            "image"
        )


class ClientProfileUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "profile",
        )

    def update(self, instance, validated_data):
        if validated_data.get("profile"):
            profile_data = validated_data.pop("profile")
            profile_serializer = ProfileUpdateSerializer(instance=instance.profile, data=profile_data)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()

        instance.save()
        return super().update(instance, validated_data)


class ClientChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientChildren
        fields = "__all__"
        extra_kwargs = {
            "parent": {"required": False}
        }