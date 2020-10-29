from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    SubscribeViewSet,
    SubscribeListView,
    FreezeRequestView,
    FreezeRequestListView
)

router = DefaultRouter()
router.register('subscriptions', SubscribeViewSet)

urlpatterns = [
    path("<uuid:uuid>/freeze", FreezeRequestView.as_view()),
    path("purchases/", SubscribeListView.as_view()),
    path("freeze-requests/", FreezeRequestListView.as_view()),
]

urlpatterns += router.urls
