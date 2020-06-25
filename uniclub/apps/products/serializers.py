from rest_framework import serializers

from .models import UniPass, Benefits


class BenefitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefits
        fields = "name",


class UniPassSerializer(serializers.ModelSerializer):
    benefits = BenefitsSerializer(many=True)

    class Meta:
        model = UniPass
        fields = "__all__"
