from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response


from .models import CityModel
from .serializers import CitySerializer


class PublicAPIMixin:
    permission_classes = []


class CityListView(PublicAPIMixin, ListAPIView):
    queryset = CityModel.objects.all()
    serializer_class = CitySerializer


class AgesView(PublicAPIMixin, APIView):
    def get(self, request, *args, **kwargs):
        return Response([i for i in range(1, 19)])
