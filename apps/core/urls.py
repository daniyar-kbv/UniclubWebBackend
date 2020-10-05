from django.urls import path, include

from .views import CityListView, AgesView

urlpatterns = [
    path("cities/", CityListView.as_view()),
    path("ages/", AgesView.as_view()),
]
