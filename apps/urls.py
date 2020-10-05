from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.authentication.urls")),
    path("website/", include("apps.website.urls")),
    path("products/", include("apps.products.urls")),
    path("clubs/", include("apps.clubs.urls")),
    path("person/", include("apps.person.urls")),
    path("study/", include("apps.grades.urls")),
    path("subscriptioins/", include("apps.subscriptions.urls")),
    path("core/", include("apps.core.urls")),
]
