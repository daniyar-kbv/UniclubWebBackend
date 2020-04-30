from django.urls import include, path

urlpatterns = [
    path("website/", include("apps.website.urls")),
    path("products/", include("apps.products.urls")),
]
