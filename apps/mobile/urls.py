from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookingApplicationViewSet, CoursesViewSet

router = DefaultRouter()

router.register('applications', BookingApplicationViewSet)
router.register('courses', CoursesViewSet)

urlpatterns = [
]

urlpatterns += router.urls
