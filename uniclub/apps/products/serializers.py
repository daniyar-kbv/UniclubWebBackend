from rest_framework import serializers

from .models import Benefits, Product


class BenefitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefits
        fields = "name",


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
