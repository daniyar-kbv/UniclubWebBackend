from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from apps.core.views import PublicAPIMixin
from apps.users.views import PartnerAPIMixin

from .models import Club
from .serializers import (
    ClubRetrieveSerializer,
    ClubListSerializer,
    ClubUpdateSerializer,
    ClubForFilterSerializer,
)
from .filters import ClubsFilterBackend


class ClubViewSet(
    PublicAPIMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = Club.objects.all()
    filter_backends = [ClubsFilterBackend]

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
        if self.request.query_params.get('favorite'):
            queryset = queryset.filter(favorite_users__id=self.request.user.id)
        return queryset.distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        context = {
            'user': request.user
        }

        if page is not None:
            serializer = self.get_serializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context=context)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated], serializer_class=None)
    def favorite(self, request, pk=None):
        try:
            club = Club.objects.get(id=pk)
        except:
            return Response('Клуб с данным id не найден', status.HTTP_404_NOT_FOUND)
        user = request.user
        if user.favorite_clubs.filter(id=pk).exists():
            user.favorite_clubs.remove(club)
        else:
            user.favorite_clubs.add(club)
        user.save()
        return Response()

    @action(detail=False, methods=['get'], filter_backends=[], pagination_class=None)
    def for_filter(self, request, pk=None):
        return Response(ClubForFilterSerializer(Club.objects.all(), many=True).data)


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
