from django.shortcuts import render
from rest_framework.generics import ListAPIView


from .models import CityModel
from .serializers import CitySerializer


class PublicAPIMixin:
    permission_classes = []


class CityListView(PublicAPIMixin, ListAPIView):
    queryset = CityModel.objects.all()
    serializer_class = CitySerializer
