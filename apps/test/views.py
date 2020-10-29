from django.db.models import Count, Q

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status

from apps.users.models import User
from apps.core.views import PublicAPIMixin
from apps.grades.models import Course, CourseReview, Coach
from apps.clubs.models import ClubReview

from .serializers import ClientCreateSerializer, PartnerCreateSerializer, CoachCreateSerializer, \
    CourseCreateSerializer, ClubReviewCreateSerializerTest, CourseReviewCreateSerializerTest


class ClientViewSet(GenericViewSet,
                    CreateModelMixin,):
    queryset = User.objects.all()
    serializer_class = ClientCreateSerializer
    permission_classes = []


class PartnerViewSet(GenericViewSet,
                     CreateModelMixin,):
    queryset = User.objects.all()
    serializer_class = PartnerCreateSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        images = request.data.pop('images')
        context = {
            'images': images
        }
        serializer = PartnerCreateSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CoachViewSet(GenericViewSet,
                   CreateModelMixin):
    queryset = Coach.objects.all()
    serializer_class = CoachCreateSerializer
    permission_classes = []


class CourseViewSet(GenericViewSet,
                    CreateModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = []


class ClubReviewViewSet(GenericViewSet,
                        CreateModelMixin):
    queryset = ClubReview.objects.all()
    serializer_class = ClubReviewCreateSerializerTest
    permission_classes = []


class CourseReviewViewSet(GenericViewSet,
                          CreateModelMixin):
    queryset = CourseReview.objects.all()
    serializer_class = CourseReviewCreateSerializerTest
    permission_classes = []


class TestView(PublicAPIMixin, APIView):
    def get(self, request, *args, **kwargs):
        # courses = Course.objects.all().annotate(attended=Count('lessons__bookings', filter=Q(lessons__bookings__user=)))
        # return Response(courses.first().attended)
        pass