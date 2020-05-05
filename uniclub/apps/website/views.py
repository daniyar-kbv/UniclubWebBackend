from rest_framework.generics import ListAPIView, CreateAPIView

from .models import FAQ, FeedBack, PartnerFeedBack
from .serializers import (
    FAQSerializer, FeedBackSerializer, PartnerFeedBackSerializer
)


class FAQListView(ListAPIView):
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()


class FeedBackPostView(CreateAPIView):
    serializer_class = FeedBackSerializer
    queryset = FeedBack.objects.all()


class PartnerFeedBackView(CreateAPIView):
    serializer_class = PartnerFeedBackSerializer
    queryset = PartnerFeedBack.objects.all()
