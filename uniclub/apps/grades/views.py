from rest_framework.viewsets import ModelViewSet

from apps.users.views import PartnerAPIMixin

from .models import Grade
from .serializers import GradeSerializer


class GradeViewSet(PartnerAPIMixin, ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_queryset(self):
        return Grade.objects.filter(club=self.get_object())

    def perform_create(self, serializer):
        serializer.save(club=self.get_object())
