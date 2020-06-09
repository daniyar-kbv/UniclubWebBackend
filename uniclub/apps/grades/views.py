from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from apps.users.views import PartnerAPIMixin

from .models import Grade, Lesson
from .serializers import GradeSerializer, LessonSerializer


class GradeViewSet(PartnerAPIMixin, ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_queryset(self):
        return Grade.objects.filter(club=self.get_object())

    def perform_create(self, serializer):
        serializer.save(club=self.get_club())


class LessonViewSet(PartnerAPIMixin, ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_grade(self):
        return get_object_or_404(
            Grade, pk=self.kwargs.get("grade_pk"), club=self.get_club()
        )

    def get_queryset(self):
        return Lesson.objects.filter(grade=self.get_grade())

    def perform_create(self, serializer):
        serializer.save(grade=self.get_grade())
