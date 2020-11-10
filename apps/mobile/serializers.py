from rest_framework import serializers

from apps.website.models import BookingApplication
from apps.grades.models import Lesson, Course, AttendanceType, LessonDay
from apps.grades.serializers import GradeTypeGroupWithTypesSerializer, AttendanceTypeSerializer, LessonDaySerializer
from apps.clubs.models import ClubImage
from apps.core.models import GradeTypeGroup
from apps.core.serializers import AdministrativeDivisionSerializer
from .models import AgeGroup


class BookingApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingApplication
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'image', 'description']

    def get_image(self, obj):
        image = obj.grade.club.images.first()
        if image:
            return self.context.get('request').build_absolute_uri(image.image.url)
        return image


class CourseRetrieveMobileSerializer(CourseListSerializer):
    images = serializers.SerializerMethodField()
    lesson_days = serializers.SerializerMethodField()

    class Meta(CourseListSerializer.Meta):
        fields = ['id', 'name', 'description', 'images', 'lesson_days']

    def get_images(self, obj):
        images = ClubImage.objects.filter(club=obj.grade.club)
        images_urls = []
        for image in images:
            images_urls.append(self.context.get('request').build_absolute_uri(image.image.url))
        return images_urls

    def get_lesson_days(self, obj):
        return [
            {
                'weekday': weekday,
                'times': LessonDaySerializer(
                    LessonDay.objects.filter(course=obj, weekday=weekday),
                    many=True
                ).data
            }
            for weekday in range(0, 7) if weekday in [lesson.weekday for lesson in LessonDay.objects.filter(course=obj, weekday=weekday)]
        ]


class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroup
        fields = ['id', 'from_age', 'to_age']


class FiltersSerializer(serializers.Serializer):
    age_groups = AgeGroupSerializer(many=True)
    attendance_types = AttendanceTypeSerializer(many=True)
    administrative_divisions = AdministrativeDivisionSerializer(many=True)
    grade_groups = AttendanceTypeSerializer(many=True)
    time_types = serializers.ListField(child=serializers.CharField())
