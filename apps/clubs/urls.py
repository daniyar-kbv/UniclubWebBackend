from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ClubViewSet, ClubUpdateView, ClubReviewViewSet

router = DefaultRouter()
router.register("", ClubViewSet)
router.register('reviews', ClubReviewViewSet)

urlpatterns = [
    path("admin/", ClubUpdateView.as_view()),
    path("", include(router.urls)),
]
