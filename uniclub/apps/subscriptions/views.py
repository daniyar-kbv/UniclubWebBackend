from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from apps.users.views import ClientAPIMixin

from .models import Subscription
from .serializers import SubscriptionCreateSerializer


class SubscribeView(ClientAPIMixin, CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionCreateSerializer
