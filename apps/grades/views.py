from django.shortcuts import get_object_or_404
from django.core.exceptions import SuspiciousOperation
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.users.views import PartnerAPIMixin, ClientAPIMixin
from apps.users.permissions import IsClient
from apps.subscriptions.models import LessonBooking
from apps.core.views import PublicAPIMixin
from apps.utils import distance

from .models import Course, Lesson, GradeType, CourseReview
from .serializers import (
    CourseSerializer, LessonSerializer, GradeTypeListSerializer, LessonRetrieveSerializer,
    CourseReviewCreateSerializer, CourseReviewSerializer, CourseReviewHelpedSerializer,
    LessonBookingCreateSerializer
)
from .filters import CoursesFilterBackend

import datetime, constants


class GradeTypesViewSet(PublicAPIMixin,
                        GenericViewSet,
                        ListModelMixin):
    queryset = GradeType.objects.all()
    serializer_class = GradeTypeListSerializer


class CourseViewSet(PartnerAPIMixin, ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        instance = self.get_club()
        serializer.save(club=instance)


class LessonViewSet(PublicAPIMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Lesson.objects.all()
    filterset_fields = ["day"]
    filter_backends = [CoursesFilterBackend]

    def get_serializer_class(self):
        if self.action == 'list':
            return LessonSerializer
        elif self.action == 'retrieve':
            return LessonRetrieveSerializer
        elif self.action == 'leave_review':
            return CourseReviewCreateSerializer
        elif self.action == 'set_status':
            return LessonBookingCreateSerializer
        return LessonSerializer

    def filter_queryset(self, queryset):
        if self.request.query_params.get('city'):
            queryset = queryset.filter(course__club__city=self.request.query_params.get('city'))
        if self.request.query_params.get('grade_type'):
            queryset = queryset.filter(course__grade_type=self.request.query_params.get('grade_type'))
        if self.request.query_params.get('club'):
            queryset = queryset.filter(course__club__id=self.request.query_params.get('club'))
        if self.request.query_params.get('age') and self.request.user is not AnonymousUser:
            queryset = queryset.filter(
                Q(course__from_age__lte=self.request.query_params.get('age')) &
                Q(course__to_age__gte=self.request.query_params.get('age'))
            )
        if self.request.query_params.get('favorite'):
            queryset = queryset.filter(favorite_users__id=self.request.user.id)
        if self.request.query_params.get('latitude') and \
            self.request.query_params.get('longitude') and \
            self.request.query_params.get('distance'):
            try:
                lat1 = float(self.request.query_params.get('latitude'))
                lon1 = float(self.request.query_params.get('longitude'))
                dis = int(self.request.query_params.get('distance'))
                for item in queryset:
                    if distance.calculate(lat1, lon1, item.course.club.latitude, item.course.club.longitude) > dis:
                        queryset = queryset.exclude(id=item.id)
            except:
                pass
        if self.request.query_params.get('date'):
            queryset = queryset.filter(day=self.request.query_params.get('date'))
        return queryset.distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        context = {
            'user': request.user
        }

        if page is not None:
            serializer = self.get_serializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context=context)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated], serializer_class=None)
    def favorite(self, request, pk=None):
        try:
            lesson = Lesson.objects.get(id=pk)
        except:
            return Response('Занятие с данным id не найден', status.HTTP_404_NOT_FOUND)
        user = request.user
        if user.favorite_lessons.filter(id=pk).exists():
            user.favorite_lessons.remove(lesson)
        else:
            user.favorite_courses.add(lesson)
        user.save()
        return Response()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def leave_review(self, request, pk=None):
        lesson = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, course=lesson.course)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], filter_backends=[], pagination_class=None)
    def more_reviews(self, request, pk=None):
        instance = self.get_object()
        serializer = CourseReviewSerializer(instance.course.reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsClient])
    def set_status(self, request, pk=None):
        instance = self.get_object()
        if instance.day < datetime.date.today() or (instance.day == datetime.date.today() and instance.end_time < datetime.datetime.now().time()):
            return Response('Это занятие уже прошло', status.HTTP_400_BAD_REQUEST)
        try:
            LessonBooking.objects.get(lesson=instance, user=request.user)
            return Response('У этого занятия уже существует статус', status.HTTP_400_BAD_REQUEST)
        except:
            pass
        serializer = LessonBookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, lesson=instance)
        return Response(serializer.data)


class CourseReviewViewSet(GenericViewSet):
    queryset = CourseReview.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'helped':
            return CourseReviewHelpedSerializer
        return CourseReviewHelpedSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def helped(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LessonBookingViewSet(ClientAPIMixin,
                           GenericViewSet):
    queryset = LessonBooking.objects.all()

    def get_queryset(self):
        return LessonBooking.objects.filter(user__in=self.get_profile().children)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        instance = self.get_object()
        instance.status = constants.LESSON_CANCELED
        instance.save()
        return Response()
