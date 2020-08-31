from rest_framework.generics import ListAPIView

from apps.core.views import PublicAPIMixin

from .models import Product
from .serializers import ProductSerializer


class ProductListView(PublicAPIMixin, ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
