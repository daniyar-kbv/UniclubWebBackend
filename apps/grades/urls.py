from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GradeViewSet, CourseViewSet, LessonViewSet, GradeTypesViewSet, CourseListViewSet, CourseReviewViewSet

grade_router = DefaultRouter()
grade_router.register("", GradeViewSet)

course_router = DefaultRouter()
course_router.register("", CourseViewSet)

course_list_router = DefaultRouter()
course_list_router.register("", CourseListViewSet)
course_list_router.register("reviews", CourseReviewViewSet)

grade_type_router = DefaultRouter()
grade_type_router.register("", GradeTypesViewSet)

lesson_router = DefaultRouter()
lesson_router.register("", LessonViewSet)

urlpatterns = [
    path("grade_types/", include(grade_type_router.urls)),
    path("grades/", include(grade_router.urls)),
    path("<int:grade_pk>/courses/", include(course_router.urls)),
    path("lessons/", include(lesson_router.urls)),
    path("courses/", include(course_list_router.urls)),
]
