from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CoachViewset, UpdateClientProfileView

router = DefaultRouter()
router.register("staff", CoachViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("client/profile/update", UpdateClientProfileView.as_view()),
]
