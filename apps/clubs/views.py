from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from apps.core.views import PublicAPIMixin
from apps.core.serializers import EmptySerializer
from apps.users.views import PartnerAPIMixin
from apps.users.permissions import IsPartner
from apps.grades.serializers import LessonClubScheduleSerializer
from apps.grades.models import Lesson
from apps.person.models import ClientChildren
from apps.subscriptions.models import Subscription

from .models import Club, ClubReview
from .serializers import (
    ClubRetrieveSerializer,
    ClubListSerializer,
    ClubUpdateSerializer,
    ClubForFilterSerializer,
    ClubReviewCreateSerializer,
    ClubReviewSerializer,
    ReviewHelpedSerializer,
    ClubScheduleSerializer,
    ClubScheduleCoachSerializer,
    ClubClientsSerializer,
)
from .filters import ClubsFilterBackend, ClubScheduleFilterBackend, ClubCalendarFilterBackend, \
    ClubScheduleWeekFilterBackend, ClubClientsFilterBackend
from dateutil.relativedelta import relativedelta
from . import ClientType

import datetime, constants, calendar


class ClubViewSet(
    PublicAPIMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    queryset = Club.objects.all()
    filter_backends = [ClubsFilterBackend]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ClubRetrieveSerializer
        elif self.action == "list":
            return ClubListSerializer
        elif self.action == 'leave_review':
            return ClubReviewCreateSerializer
        elif self.action == 'admin':
            return ClubUpdateSerializer
        elif self.action == 'schedule_main':
            return LessonClubScheduleSerializer
        elif self.action == 'calendar':
            return EmptySerializer
        elif self.action == 'clients':
            return ClubClientsSerializer
        return ClubListSerializer

    def filter_queryset(self, queryset):
        if self.request.query_params.get('city'):
            queryset = queryset.filter(city_id=self.request.query_params.get('city'))
        if self.request.query_params.get('grade_type'):
            queryset = queryset.filter(courses__grade_type=self.request.query_params.get('grade_type'))
        if self.request.query_params.get('club'):
            queryset = queryset.filter(id=self.request.query_params.get('club'))
        if self.request.query_params.get('age'):
            queryset = queryset.filter(
                Q(from_age__lte=self.request.query_params.get('age')) &
                Q(to_age__gte=self.request.query_params.get('age'))
            )
        if self.request.query_params.get('favorite'):
            queryset = queryset.filter(favorite_users__id=self.request.user.id)
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
            club = Club.objects.get(id=pk)
        except:
            return Response('Клуб с данным id не найден', status.HTTP_404_NOT_FOUND)
        user = request.user
        if user.favorite_clubs.filter(id=pk).exists():
            user.favorite_clubs.remove(club)
        else:
            user.favorite_clubs.add(club)
        user.save()
        return Response()

    @action(detail=False, methods=['get'], filter_backends=[], pagination_class=None)
    def for_filter(self, request, pk=None):
        return Response(ClubForFilterSerializer(Club.objects.all(), many=True).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def leave_review(self, request, pk=None):
        club = self.get_object()
        serializer = ClubReviewCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, club=club)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], filter_backends=[], pagination_class=None)
    def more_reviews(self, request, pk=None):
        instance = self.get_object()
        serializer = ClubReviewSerializer(instance.reviews, many=True)
        return Response(serializer.data)

    @action(detail=False,
            methods=['get', 'post'],
            filter_backends=[],
            pagination_class=None,
            permission_classes=[IsPartner])
    def admin(self, request, pk=None):
        instance = self.request.user.club
        if request.method == 'GET':
            serializer = ClubUpdateSerializer(instance)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = ClubUpdateSerializer(data=request.data, instance=instance, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False,
            methods=['get'],
            filter_backends=[ClubScheduleFilterBackend],
            pagination_class=None,
            permission_classes=[IsPartner])
    def schedule_main(self, request, pk=None):
        instance = self.request.user.club
        try:
            date = datetime.datetime.strptime(self.request.query_params.get('date'), constants.DATE_FORMAT) \
                if self.request.query_params.get('date') \
                else datetime.date.today()
        except:
            date = datetime.date.today()
        lessons = Lesson.objects.filter(course__club=instance, day=date).order_by('start_time')
        serializer = LessonClubScheduleSerializer(lessons, many=True)
        return Response({
            'date': datetime.date.today().strftime(constants.DATE_FORMAT),
            'lessons': serializer.data
        })

    @action(detail=False,
            methods=['get'],
            filter_backends=[ClubCalendarFilterBackend],
            pagination_class=None,
            permission_classes=[IsPartner])
    def calendar(self, request, pk=None):
        try:
            year = int(self.request.query_params.get('year')) \
                if self.request.query_params.get('year') \
                else datetime.date.today().year
            month = int(self.request.query_params.get('month')) \
                if self.request.query_params.get('month') \
                else datetime.date.today().month
        except:
            year = datetime.date.today().year
            month = datetime.date.today().month
        calendar_month = calendar.monthcalendar(year=year, month=month)
        days = []
        for index, week in enumerate(calendar_month):
            for index2, day in enumerate(calendar_month[index]):
                if day != 0:
                    days.append({
                        'weekday': index2,
                        'day': day,
                        'is_today': datetime.date.today().year == year and
                                    datetime.date.today().month == month and
                                    datetime.date.today().day == day
                    })
        return Response({
            'year': year,
            'month': month,
            'days': days
        })

    @action(detail=False,
            methods=['get'],
            filter_backends=[ClubScheduleWeekFilterBackend],
            pagination_class=None,
            permission_classes=[IsPartner])
    def schedule_week(self, request, pk=None):
        instance = self.request.user.club
        dt = datetime.date.today()
        start = dt - datetime.timedelta(days=dt.weekday())
        end = start + datetime.timedelta(days=6)
        if self.request.query_params.get('from_date') and self.request.query_params.get('to_date'):
            try:
                start = datetime.datetime.strptime(
                    self.request.query_params.get('from_date'), constants.DATE_FORMAT
                ).date()
            except:
                return Response({
                    'start_time': 'Формат времени: YYYY-MM-DD'
                })
            try:
                end = datetime.datetime.strptime(
                    self.request.query_params.get('to_date'), constants.DATE_FORMAT
                ).date()
            except:
                return Response({
                    'start_time': 'Формат времени: YYYY-MM-DD'
                })
        delta = (end + datetime.timedelta(days=1)) - start
        dates = [start + datetime.timedelta(days=i) for i in range(delta.days)]
        context = {
            'club': instance
        }
        serializer = ClubScheduleSerializer(dates, many=True, context=context)
        return Response(serializer.data)

    @action(detail=False,
            methods=['get'],
            filter_backends=[ClubScheduleFilterBackend],
            pagination_class=None,
            permission_classes=[IsPartner])
    def schedule_day(self, request, pk=None):
        instance = self.request.user.club
        try:
            date = datetime.datetime.strptime(self.request.query_params.get('date'), constants.DATE_FORMAT) \
                if self.request.query_params.get('date') \
                else datetime.date.today()
        except:
            date = datetime.date.today()
        context = {
            'club': instance,
            'date': date
        }
        coaches = instance.coaches
        serializer = ClubScheduleCoachSerializer(coaches, many=True, context=context)
        return Response({
            'date': date,
            'coaches': serializer.data
        })

    @action(detail=False,
            methods=['get'],
            filter_backends=[ClubClientsFilterBackend],
            pagination_class=None,
            permission_classes=[IsPartner])
    def clients(self, request, pk=None):
        clients_type = self.request.query_params.get('type') \
            if self.request.query_params.get('type') \
            else ClientType.ALL
        instance = self.request.user.club
        children = ClientChildren.objects.filter(lesson_statuses__lesson__course__club=instance)
        if clients_type != ClientType.ALL:
            for child in children:
                last_subscription = Subscription.objects.filter(child=child).order_by('-created_at').first()
                if last_subscription.product.product_type != clients_type:
                    children.exclude(id=child.id)
        serializer = ClubClientsSerializer(children, many=True)
        return Response(serializer.data)


class ClubReviewViewSet(GenericViewSet):
    queryset = ClubReview.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'helped':
            return ReviewHelpedSerializer
        return ReviewHelpedSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def helped(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
