from django.urls import path

from .views import UniPassListView

urlpatterns = [
    path("subscriptions/", UniPassListView.as_view()),
]
