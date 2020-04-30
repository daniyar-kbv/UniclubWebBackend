from rest_framework.generics import ListAPIView, CreateAPIView

from .models import FAQ, FeedBack
from .serializers import FAQSerializer, FeedBackSerializer


class FAQListView(ListAPIView):
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()


class FeedBackPostView(CreateAPIView):
    serializer_class = FeedBackSerializer
    queryset = FeedBack.objects.all()
