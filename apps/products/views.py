from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.views import PublicAPIMixin

from .models import Product
from .serializers import ProductSerializer, ProductTypesSerializer
from . import ProductType


class ProductListViewSet(PublicAPIMixin,
                      GenericViewSet,
                      ListModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'types':
            return ProductTypesSerializer
        return ProductSerializer

    @action(detail=False, methods=['get'])
    def types(self, request, pk=None):
        types = []
        for type_ in ProductType:
            types.append(type_)
        return Response({
            'types': types
        })
