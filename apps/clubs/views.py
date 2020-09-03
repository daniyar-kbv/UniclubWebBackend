from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from apps.core.views import PublicAPIMixin
from apps.users.views import PartnerAPIMixin

from .models import Club
from .serializers import (
    ClubRetrieveSerializer,
    ClubListSerializer,
    ClubUpdateSerializer,
)


class ClubViewSet(
    PublicAPIMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = Club.objects.all()

    def get_serializer_class(self):
        print(self.action)
        if self.action == "retrieve":
            return ClubRetrieveSerializer
        if self.action == "list":
            return ClubListSerializer
        return ClubListSerializer


class ClubUpdateView(
    PartnerAPIMixin, APIView
):
    @swagger_auto_schema(
        responses={200: ClubUpdateSerializer}
    )
    def get(self, request, *args, **kwargs):
        """
        Получение данных клуба (для админа клуба)
        """
        instance = self.get_club()
        serializer = ClubUpdateSerializer(instance)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ClubUpdateSerializer, responses={200: ClubUpdateSerializer}
    )
    def post(self, request, *args, **kwargs):
        """
        Редактирование данных клуба (для админа клуба)
        """
        instance = self.get_club()
        serializer = ClubUpdateSerializer(data=request.data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
