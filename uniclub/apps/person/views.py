from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from apps.users.views import PartnerAPIMixin

from .serializers import CoachSerializer
from .models import Coach


class CoachViewset(PartnerAPIMixin, ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer

    def get_queryset(self):
        return Coach.objects.filter(club=self.get_club())

    def perform_create(self, serializer):
        serializer.save(club=self.get_club())
