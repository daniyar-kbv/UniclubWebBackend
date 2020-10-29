from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.decorators import action

from apps.users.views import ClientAPIMixin

from .models import Subscription, FreezeRequest
from .serializers import (
    SubscriptionCreateSerializer,
    SubscriptionListSerializer,
    FreezeRequestSerializer
)


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
