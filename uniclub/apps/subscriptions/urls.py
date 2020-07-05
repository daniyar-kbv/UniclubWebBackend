from django.urls import path

from .views import SubscribeView, FreezeRequestView

urlpatterns = [
    path("registration", SubscribeView.as_view()),
    path("<uuid:uuid>/freeze", FreezeRequestView.as_view()),
]
