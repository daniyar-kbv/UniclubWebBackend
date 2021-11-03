from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.decorators import action
from rest_framework import serializers

from apps.users.views import ClientAPIMixin, PartnerAPIMixin
from apps.users.permissions import IsClient, IsPartner

from .models import Subscription, FreezeRequest, LessonBooking
from .serializers import (
    SubscriptionCreateSerializer,
    SubscriptionListSerializer,
    FreezeRequestSerializer,
    LessonBookingUpdateSerializer,
    LessonStatusesSerializer
)
from . import LessonStatuses


class SubscribeViewSet(ClientAPIMixin,
                       GenericViewSet,
                       CreateModelMixin):
    queryset = Subscription.objects.all()

    def get_serializer_class(self):
        return SubscriptionCreateSerializer


class FreezeRequestView(ClientAPIMixin, APIView):
    def post(self, request, uuid):
        FreezeRequest.objects.create(
            customer=request.user,
            subscription_id=uuid
        )

        return Response(status=201)


class SubscribeListView(ClientAPIMixin, ListAPIView):
    serializer_class = SubscriptionListSerializer

    def get_queryset(self):
        return Subscription.objects.filter(customer=self.request.user)


class FreezeRequestListView(ClientAPIMixin, APIView):
    serializer_class = FreezeRequestSerializer

    def get_queryset(self):
        return FreezeRequest.objects.filter(customer=self.request.user)


class LessonBookingViewSet(GenericViewSet,
                           UpdateModelMixin,
                           PartnerAPIMixin):
    queryset = LessonBooking.objects.all()

    def get_serializer_class(self):
        if self.action == 'statuses':
            return LessonStatusesSerializer
        return LessonBookingUpdateSerializer

    @action(detail=False, methods=['get'], pagination_class=None)
    def statuses(self, request, pk=None):
        serializer = LessonStatusesSerializer(LessonStatuses)
        return Response(serializer.data)
