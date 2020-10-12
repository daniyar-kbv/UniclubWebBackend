from django.urls import path, include

from .views import CityListView, AgesView, DatesView

urlpatterns = [
    path("cities/", CityListView.as_view()),
    path("ages/", AgesView.as_view()),
    path("dates/", DatesView.as_view()),
]
