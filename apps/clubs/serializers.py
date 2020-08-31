from rest_framework import serializers

from .models import Club, ClubImage


class ClubImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubImage
        fields = "image",


class ClubRetrieveSerializer(serializers.ModelSerializer):
    images = ClubImageSerializer(many=True)

    class Meta:
        model = Club
        fields = "__all__"


class ClubListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = (
            "id",
            "name",
            "short_description",
            "address",
            "longitude",
            "latitude",
            "image",
        )


class ClubUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        exclude = "club_admin",
