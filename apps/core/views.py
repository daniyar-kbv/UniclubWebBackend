from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import CityModel
from .serializers import CitySerializer

import constants


class PublicAPIMixin:
    permission_classes = []


class CityListView(PublicAPIMixin, ListAPIView):
    queryset = CityModel.objects.all()
    serializer_class = CitySerializer


class AgesView(PublicAPIMixin, APIView):
    def get(self, request, *args, **kwargs):
        return Response([i for i in range(1, 19)])


class DatesView(PublicAPIMixin, APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            [{
                'date': (timezone.now() + timezone.timedelta(days=i)).strftime(constants.DATE_FORMAT),
                'weekday': (timezone.now() + timezone.timedelta(days=i)).weekday()
            } for i in range(0, 28)]
        )
