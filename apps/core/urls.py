from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AgesView, DatesView, AttendanceTypeView, CityListViewSet

router = DefaultRouter()
router.register('cities', CityListViewSet)

urlpatterns = [
    path("ages/", AgesView.as_view()),
    path("dates/", DatesView.as_view()),
    path("attendance_types/", AttendanceTypeView.as_view()),
]

urlpatterns += router.urls
