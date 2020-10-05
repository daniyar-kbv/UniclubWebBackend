from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend
from drf_yasg.utils import swagger_auto_schema

from apps.core.views import PublicAPIMixin
from apps.users.views import PartnerAPIMixin

from .models import Club
from .serializers import (
    ClubRetrieveSerializer,
    ClubListSerializer,
    ClubUpdateSerializer,
)

import coreapi


class SimpleFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='city',
                location='query',
                required=False,
                type='int',
                example=1
            ),
            coreapi.Field(
                name='grade_type',
                location='query',
                required=False,
                type='int',
                example=1
            ),
            coreapi.Field(
                name='club',
                location='query',
                required=False,
                type='int',
                example=1
            ),
            coreapi.Field(
                name='age',
                location='query',
                required=False,
                type='int',
                example=1
            ),
        ]


class ClubViewSet(
    PublicAPIMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = Club.objects.all()
    filter_backends = [SimpleFilterBackend]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ClubRetrieveSerializer
        if self.action == "list":
            return ClubListSerializer
        return ClubListSerializer

    def filter_queryset(self, queryset):
        if self.request.query_params.get('city'):
            queryset = queryset.filter(city_id=self.request.query_params.get('city'))
        if self.request.query_params.get('grade_type'):
            queryset = queryset.filter(grades__grade_type=self.request.query_params.get('grade_type'))
        if self.request.query_params.get('club'):
            queryset = queryset.filter(id=self.request.query_params.get('club'))
        if self.request.query_params.get('age'):
            queryset = queryset.filter(
                Q(from_age__lte=self.request.query_params.get('age')) &
                Q(to_age__gte=self.request.query_params.get('age'))
            )
        return queryset.distinct()


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
