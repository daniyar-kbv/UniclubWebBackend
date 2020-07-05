from django.urls import path

from .views import SubscribeView

urlpatterns = [
    path("registration", SubscribeView.as_view()),
]
