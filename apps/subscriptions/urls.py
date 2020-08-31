from django.urls import path

from .views import (
    SubscribeView,
    SubscribeListView,
    FreezeRequestView,
    FreezeRequestListView
)

urlpatterns = [
    path("registration", SubscribeView.as_view()),
    path("<uuid:uuid>/freeze", FreezeRequestView.as_view()),
    path("purchases/", SubscribeListView.as_view()),
    path("freeze-requests/", FreezeRequestListView.as_view()),
]
