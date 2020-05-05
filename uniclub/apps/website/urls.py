from django.urls import path

from .views import (
    FAQListView, FeedBackPostView, PartnerFeedBackView
)

urlpatterns = [
    path("faq/", FAQListView.as_view()),
    path("feedback/", FeedBackPostView.as_view()),
    path("feedback/partner/", PartnerFeedBackView.as_view()),
]
