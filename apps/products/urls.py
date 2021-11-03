from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import ProductListViewSet

router = DefaultRouter()

router.register('', ProductListViewSet)

urlpatterns = [
]

urlpatterns += router.urls
