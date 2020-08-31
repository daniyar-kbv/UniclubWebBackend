from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CoachViewset,
    ChildrenViewSet,
    UpdateClientProfileView
)

router = DefaultRouter()
router.register("staff", CoachViewset)
router.register("children", ChildrenViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("client/profile/update", UpdateClientProfileView.as_view()),
]
