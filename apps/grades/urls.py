from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GradeViewSet, CourseViewSet, LessonViewSet

grade_router = DefaultRouter()
grade_router.register("", GradeViewSet)

course_router = DefaultRouter()
course_router.register("", CourseViewSet)

urlpatterns = [
    path("grades/", include(grade_router.urls)),
    path("<int:grade_pk>/courses", include(course_router.urls)),
    path("lessons/", LessonViewSet.as_view()),
]
