from django.urls import path
from .views import ClientViewSet, PartnerViewSet, CoachViewSet, GradeViewSet, CourseViewSet, ClubReviewViewSet, \
    CourseReviewViewSet
from rest_framework import routers

urlpatterns = [
]

router = routers.DefaultRouter()
router.register('clients', ClientViewSet)
router.register('partners', PartnerViewSet)
router.register('coaches', CoachViewSet)
router.register('grades', GradeViewSet)
router.register('courses', CourseViewSet)
router.register('club_reviews', ClubReviewViewSet)
router.register('course_reviews', CourseReviewViewSet)

urlpatterns += router.urls