from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GradeViewSet, CourseViewSet, LessonViewSet, GradeTypesViewSet, CourseListViewSet

grade_router = DefaultRouter()
grade_router.register("", GradeViewSet)

course_router = DefaultRouter()
course_router.register("", CourseViewSet)

course_list_router = DefaultRouter()
course_list_router.register("", CourseListViewSet)

grade_type_router = DefaultRouter()
grade_type_router.register("", GradeTypesViewSet)

urlpatterns = [
    path("grade_types/", include(grade_type_router.urls)),
    path("grades/", include(grade_router.urls)),
    path("<int:grade_pk>/courses", include(course_router.urls)),
    path("lessons/", LessonViewSet.as_view()),
    path("courses/", include(course_list_router.urls)),
]
