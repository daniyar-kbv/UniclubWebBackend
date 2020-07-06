from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView

from apps.users.views import ClientAPIMixin

from .models import Subscription, FreezeRequest
from .serializers import (
    SubscriptionCreateSerializer, SubscriptionListSerializer
)


class SubscribeView(ClientAPIMixin, CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionCreateSerializer


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
