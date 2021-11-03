from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import action

from .models import CityModel, AdministrativeDivision
from .serializers import CitySerializer, AdministrativeDivisionSerializer

import constants


class PublicAPIMixin:
    permission_classes = []


class CityListViewSet(PublicAPIMixin,
                   GenericViewSet,
                   ListModelMixin):
    queryset = CityModel.objects.all()

    def get_serializer_class(self):
        if self.action == 'administrative_divisions':
            return AdministrativeDivisionSerializer
        return CitySerializer


    @action(detail=True, methods=['get'])
    def administrative_divisions(self, request, pk=None):
        city = self.get_object()
        serializer = AdministrativeDivisionSerializer(city.administrative_divisions, many=True)
        return Response(serializer.data)



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


