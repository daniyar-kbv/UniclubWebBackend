from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, LessonViewSet, GradeTypesViewSet, CourseReviewViewSet, LessonBookingViewSet

course_router = DefaultRouter()
course_router.register("", CourseViewSet)

course_list_router = DefaultRouter()
course_list_router.register("reviews", CourseReviewViewSet)

grade_type_router = DefaultRouter()
grade_type_router.register("", GradeTypesViewSet)

lesson_router = DefaultRouter()
lesson_router.register("", LessonViewSet)

lesson_booking_router = DefaultRouter()
lesson_booking_router.register("", LessonBookingViewSet)

urlpatterns = [
    path("grade_types/", include(grade_type_router.urls)),
    path("courses/", include(course_router.urls)),
    path("lessons/", include(lesson_router.urls)),
    path("lesson_bookings/", include(lesson_booking_router.urls)),
]
