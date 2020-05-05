from rest_framework import serializers

from .models import Club


class ClubRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = "__all__"


class ClubListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = (
            "name",
            "short_description",
            "address",
            "longitude",
            "latitude",
            "image",
        )
