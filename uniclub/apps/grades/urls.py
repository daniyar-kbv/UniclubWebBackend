from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GradeViewSet, LessonViewSet

router = DefaultRouter()
router.register("<int:grade_pk>/lessons", LessonViewSet)
router.register("grades", GradeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
