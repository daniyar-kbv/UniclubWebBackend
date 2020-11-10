from rest_framework import serializers

from . models import CityModel, AdministrativeDivision


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityModel
        fields = (
            "id",
            "name"
        )


class EmptySerializer(serializers.BaseSerializer):
    pass


class AdministrativeDivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeDivision
        fields = ['id', 'name']
