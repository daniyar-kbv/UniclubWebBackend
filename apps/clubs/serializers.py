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
            "is_new",
        )


class ClubForFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = (
            "id",
            "name",
        )


class ClubUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        exclude = "club_admin",

    def validate(self, data):
        if data.get('from_age') < 1 or data.get('from_age') > 18 or data.get('to_age') < 1 or data.get('to_age') > 18:
            raise serializers.ValidationError("Диапозон возраста: 1 - 18")
        if data.get('from_age') > data.get('to_age'):
            raise serializers.ValidationError("Возраст от должен быть меньше чем возраст до")
        return data
