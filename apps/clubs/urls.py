from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ClubViewSet, ClubReviewViewSet

router = DefaultRouter()
router.register("", ClubViewSet)
router.register('reviews', ClubReviewViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
