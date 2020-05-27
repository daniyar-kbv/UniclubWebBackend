from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CoachViewset

router = DefaultRouter()
router.register("staff", CoachViewset)

urlpatterns = [
    path("", include(router.urls)),
]
