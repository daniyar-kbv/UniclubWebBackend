from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CoachViewset,
    ChildrenViewSet,
    UpdateClientProfileViewSet
)

router = DefaultRouter()
router.register("staff", CoachViewset)
router.register("children", ChildrenViewSet)
router.register('client_profile', UpdateClientProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
