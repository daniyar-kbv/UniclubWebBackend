from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.users.views import PartnerAPIMixin, ClientAPIMixin

from .serializers import CoachSerializer, ClientProfileUpdateSerializer
from .models import Coach

User = get_user_model()


class CoachViewset(PartnerAPIMixin, ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer

    def get_queryset(self):
        return Coach.objects.filter(club=self.get_club())

    def perform_create(self, serializer):
        serializer.save(club=self.get_club())


class UpdateClientProfileView(ClientAPIMixin, APIView):
    @swagger_auto_schema(
        request_body=ClientProfileUpdateSerializer,
        responses={200: ClientProfileUpdateSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = ClientProfileUpdateSerializer(
            instance=request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
