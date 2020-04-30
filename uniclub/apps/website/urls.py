from django.urls import path

from .views import FAQListView, FeedBackPostView

urlpatterns = [
    path("faq/", FAQListView.as_view()),
    path("feedback/", FeedBackPostView.as_view()),
]
