from rest_framework.generics import ListAPIView

from apps.core.views import PublicAPIMixin

from .models import UniPass
from .serializers import UniPassSerializer


class UniPassListView(PublicAPIMixin, ListAPIView):
    serializer_class = UniPassSerializer
    queryset = UniPass.objects.all()
