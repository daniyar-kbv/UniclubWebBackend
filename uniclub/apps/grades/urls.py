from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GradeViewSet, LessonViewSet

grade_router = DefaultRouter()
grade_router.register("", GradeViewSet)

lesson_router = DefaultRouter()
lesson_router.register("", LessonViewSet)

urlpatterns = [
    path("grades/", include(grade_router.urls)),
    path("<int:grade_pk>/lessons", include(lesson_router.urls)),
]
