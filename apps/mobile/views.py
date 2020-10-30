from django.db.models import Q

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from apps.website.models import BookingApplication
from apps.core.models import GradeTypeGroup
from apps.grades.models import Lesson, AttendanceType, Course
from apps.grades.serializers import GradeTypeGroupWithTypesSerializer, AttendanceTypeSerializer
from .serializers import BookingApplicationCreateSerializer, CourseListSerializer, AgeGroupSerializer, \
    FiltersSerializer, CourseRetrieveMobileSerializer
from .models import AgeGroup
from .filters import CoursesMobileFilterBackend

import constants, datetime


class CoursesViewSet(GenericViewSet,
                     ListModelMixin,
                     RetrieveModelMixin):
    queryset = Course.objects.all()
    permission_classes = []
    filter_backends = [CoursesMobileFilterBackend]

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        elif self.action == 'retrieve':
            return CourseRetrieveMobileSerializer
        elif self.action == 'filter_data':
            return FiltersSerializer
        return CourseListSerializer

    def filter_queryset(self, queryset):
        if self.request.query_params.get('age_group'):
            try:
                age_group = AgeGroup.objects.get(id=self.request.query_params.get('age_group'))
                queryset = queryset.filter(
                    Q(from_age__lte=age_group.to_age) | Q(to_age__gte=age_group.from_age)
                )
            except:
                pass
        if self.request.query_params.get('attendance_type'):
            queryset = queryset.filter(attendance_type=self.request.query_params.get('attendance_type'))
        if self.request.query_params.get('grade_type'):
            queryset = queryset.filter(grade__grade_type__id=self.request.query_params.get('grade_type'))
        if self.request.query_params.get('time'):
            if self.request.query_params.get('time') == constants.TIME_BEFORE_LUNCH:
                queryset = queryset.filter(lessons_start_time__lte=datetime.time(hour=12, minute=0, second=0))
            elif self.request.query_params.get('time') == constants.TIME_AFTER_LUNCH:
                queryset = queryset.filter(lessons_start_time__gte=datetime.time(hour=12, minute=0, second=0))
        return queryset.distinct()

    @action(detail=False, methods=['get'], filter_backends=[], pagination_class=None)
    def filter_data(self, request, pk=None):
        ages = AgeGroup.objects.all()
        age_serializer = AgeGroupSerializer(ages, many=True)
        attendance_types = AttendanceType.objects.all()
        attendance_serializer = AttendanceTypeSerializer(attendance_types, many=True)
        grade_groups = GradeTypeGroup.objects.all()
        grage_serializer = GradeTypeGroupWithTypesSerializer(grade_groups, many=True)
        data = {
            'age_groups': age_serializer.data,
            'attendance_types': attendance_serializer.data,
            'grade_groups': grage_serializer.data,
            'time_types': constants.TIMES
        }
        return Response(data)


class BookingApplicationViewSet(GenericViewSet,
                                CreateModelMixin):
    queryset = BookingApplication.objects.all()
    permission_classes = []

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingApplicationCreateSerializer
        return BookingApplicationCreateSerializer
