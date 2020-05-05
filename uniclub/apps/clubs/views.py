from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from .models import Club
from .serializers import ClubRetrieveSerializer, ClubListSerializer


class ClubViewSet(
    ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = Club.objects.all()

    def get_serializer_class(self):
        print(self.action)
        if self.action == "retrieve":
            return ClubRetrieveSerializer
        if self.action == "list":
            return ClubListSerializer
        return ClubListSerializer
