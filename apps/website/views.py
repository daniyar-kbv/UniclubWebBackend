from rest_framework.generics import ListAPIView, CreateAPIView

from apps.core.views import PublicAPIMixin
from .models import FAQ, FeedBack, PartnerFeedBack
from .serializers import (
    FAQSerializer, FeedBackSerializer, PartnerFeedBackSerializer
)


class FAQListView(PublicAPIMixin, ListAPIView):
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()


class FeedBackPostView(PublicAPIMixin, CreateAPIView):
    serializer_class = FeedBackSerializer
    queryset = FeedBack.objects.all()


class PartnerFeedBackView(PublicAPIMixin, CreateAPIView):
    serializer_class = PartnerFeedBackSerializer
    queryset = PartnerFeedBack.objects.all()
