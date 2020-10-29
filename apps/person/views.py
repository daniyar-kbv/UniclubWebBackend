from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.users.views import PartnerAPIMixin, ClientAPIMixin
from apps.grades.models import Coach
from apps.subscriptions.serializers import SubscriptionProfileSerializer
from apps.subscriptions.models import Subscription
from apps.subscriptions import SubscriptionStatuses

from .models import ClientChildren, ClientProfile
from .serializers import (
    CoachSerializer,
    ClientProfileUpdateSerializer,
    ClientChildrenSerializer,
    ScheduleSerializer
)
from .filters import ScheduleFilterBackend

import datetime, constants

User = get_user_model()


class CoachViewset(PartnerAPIMixin, ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer

    def get_queryset(self):
        return Coach.objects.filter(club=self.get_club())

    def perform_create(self, serializer):
        serializer.save(club=self.get_club())


class UpdateClientProfileViewSet(ClientAPIMixin,
                                 GenericViewSet,
                                 RetrieveModelMixin,
                                 UpdateModelMixin):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update']:
            return ClientProfileUpdateSerializer
        return ClientProfileUpdateSerializer


class ChildrenViewSet(ClientAPIMixin, ModelViewSet):
    queryset = ClientChildren.objects.all()

    def get_serializer_class(self):
        if self.action == 'schedule':
            return ScheduleSerializer
        if self.action == 'subscriptions':
            return SubscriptionProfileSerializer
        return ClientChildrenSerializer

    def get_queryset(self):
        return ClientChildren.objects.filter(parent=self.get_profile())

    def perform_create(self, serializer):
        serializer.save(parent=self.get_profile())

    def filter_queryset(self, queryset):
        return queryset

    @action(detail=True, methods=['get'], filter_backends=[ScheduleFilterBackend])
    def schedule(self, request, pk=None):
        child = self.get_object()
        dt = datetime.date.today()
        start = dt - datetime.timedelta(days=dt.weekday())
        end = start + datetime.timedelta(days=6)
        if self.request.query_params.get('from_date') and self.request.query_params.get('to_date'):
            try:
                start = datetime.datetime.strptime(
                    self.request.query_params.get('from_date'), constants.DATE_FORMAT
                ).date()
            except:
                return Response({
                    'start_time': 'Формат времени: YYYY-MM-DD'
                })
            try:
                end = datetime.datetime.strptime(
                    self.request.query_params.get('to_date'), constants.DATE_FORMAT
                ).date()
            except:
                return Response({
                    'start_time': 'Формат времени: YYYY-MM-DD'
                })
        delta = (end + datetime.timedelta(days=1)) - start
        dates = [start + datetime.timedelta(days=i) for i in range(delta.days)]
        context = {
            'child': child
        }
        serializer = ScheduleSerializer(dates, many=True, context=context)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], filter_backends=[ScheduleFilterBackend])
    def subscriptions(self, request, pk=None):
        child = self.get_object()
        subscriptions = Subscription.objects.filter(child=child, status=SubscriptionStatuses.ACTIVE)
        serializer = SubscriptionProfileSerializer(subscriptions, many=True)
        return Response(serializer.data)

