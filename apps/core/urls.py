from django.urls import path, include

from .views import CityListView, AgesView, DatesView, AttendanceTypeView

urlpatterns = [
    path("cities/", CityListView.as_view()),
    path("ages/", AgesView.as_view()),
    path("dates/", DatesView.as_view()),
    path("attendance_types/", AttendanceTypeView.as_view()),
]
