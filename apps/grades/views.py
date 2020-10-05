from django.shortcuts import get_object_or_404
from django.core.exceptions import SuspiciousOperation
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import ListAPIView

from apps.users.views import PartnerAPIMixin
from apps.core.views import PublicAPIMixin
from apps.clubs.views import SimpleFilterBackend

from .models import Grade, Course, Lesson, GradeType
from .serializers import (
    GradeSerializer, CourseSerializer, LessonSerializer, GradeTypeListSerializer
)


class GradeTypesViewSet(PublicAPIMixin,
                        GenericViewSet,
                        ListModelMixin):
    queryset = GradeType.objects.all()
    serializer_class = GradeTypeListSerializer


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


class CourseListViewSet(PartnerAPIMixin, ListModelMixin, GenericViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [SimpleFilterBackend]

    def filter_queryset(self, queryset):
        if self.request.query_params.get('city'):
            queryset = queryset.filter(grade__club__city=self.request.query_params.get('city'))
        if self.request.query_params.get('grade_type'):
            queryset = queryset.filter(grade__grade_type=self.request.query_params.get('grade_type'))
        if self.request.query_params.get('club'):
            queryset = queryset.filter(grade__club__id=self.request.query_params.get('club'))
        if self.request.query_params.get('age'):
            queryset = queryset.filter(
                Q(from_age__lte=self.request.query_params.get('age')) &
                Q(to_age__gte=self.request.query_params.get('age'))
            )
        return queryset.distinct()


class LessonViewSet(PublicAPIMixin, ListAPIView):
    filter_backends = [DjangoFilterBackend]
    queryset = Lesson.objects.all()
    filterset_fields = ["day"]
    serializer_class = LessonSerializer
