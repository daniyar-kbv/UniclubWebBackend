from django.urls import path

from .views import (
    SubscribeView, FreezeRequestView, SubscribeListView
)

urlpatterns = [
    path("registration", SubscribeView.as_view()),
    path("<uuid:uuid>/freeze", FreezeRequestView.as_view()),
    path("purchases/", SubscribeListView.as_view()),
]
