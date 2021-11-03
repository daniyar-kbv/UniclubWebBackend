from django.urls import path
from .views import ClientViewSet, PartnerViewSet, CoachViewSet, CourseViewSet, ClubReviewViewSet, \
    CourseReviewViewSet, TestView
from rest_framework import routers

urlpatterns = [
    path('test/', TestView.as_view())
]

router = routers.DefaultRouter()
router.register('clients', ClientViewSet)
router.register('partners', PartnerViewSet)
router.register('coaches', CoachViewSet)
router.register('courses', CourseViewSet)
router.register('club_reviews', ClubReviewViewSet)
router.register('course_reviews', CourseReviewViewSet)

urlpatterns += router.urls