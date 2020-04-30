from rest_framework.generics import ListAPIView

from .models import UniPass
from .serializers import UniPassSerializer


class UniPassListView(ListAPIView):
    serializer_class = UniPassSerializer
    queryset = UniPass.objects.all()
