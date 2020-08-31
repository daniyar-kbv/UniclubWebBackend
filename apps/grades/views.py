from django.shortcuts import get_object_or_404
from django.core.exceptions import SuspiciousOperation
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView


from apps.users.views import PartnerAPIMixin
from apps.core.views import PublicAPIMixin

from .models import Grade, Course, Lesson
from .serializers import (
    GradeSerializer, CourseSerializer, LessonSerializer
)


class GradeViewSet(PartnerAPIMixin, ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_queryset(self):
        return Grade.objects.filter(club=self.get_club())

    def perform_create(self, serializer):
        serializer.save(club=self.get_club())


class CourseViewSet(PartnerAPIMixin, ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_grade(self):
        return get_object_or_404(
            Grade, pk=self.kwargs.get("grade_pk"), club=self.get_club()
        )

    def get_queryset(self):
        return Course.objects.filter(grade=self.get_grade())

    def perform_create(self, serializer):
        serializer.save(grade=self.get_grade())


class LessonViewSet(PublicAPIMixin, ListAPIView):
    filter_backends = [DjangoFilterBackend]
    queryset = Lesson.objects.all()
    filterset_fields = ["day"]
    serializer_class = LessonSerializer
