from django.db import transaction
from rest_framework import serializers

from apps.clubs.models import Club, ClubReview, ClubImage
from apps.users.serializers import UserShortSerializer
from apps.utils import general
from .models import Grade, Course, LessonDay, Lesson, GradeType, CourseReview, GradeTypeGroup, AttendanceType, \
    LessonUserStatus, Coach

import constants


class CoachClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        exclude = ['club', 'course']


class ClubReviewSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()

    class Meta:
        model = ClubReview
        exclude = ['club']


class ClubImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubImage
        fields = "image",


class ClubRetrieveSerializer(serializers.ModelSerializer):
    images = ClubImageSerializer(many=True)

    class Meta:
        model = Club
        fields = ["id", "images", "address", "latitude", "longitude", "instagram", "facebook", "vk", "mobile_phone",
                  "home_phone", "work_phone", "email", "website", "image", "short_description", "description",
                  "competition_frequency", "hazard_information", "student_achievements", "events_information",
                  "other_services", "parking_available", "places_for_parents", "parent_presence", "video_monitoring",
                  "classes_for_disabled", "floor_area", "number_of_bathrooms", "number_of_changing_rooms",
                  "total_number_of_students", "social_reviews", "from_age", "to_age", "is_new", "name", "city",
                  "club_admin"]


class GradeTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeType
        exclude = ['group']


class GradeTypeGroupWithTypesSerializer(serializers.ModelSerializer):
    types = GradeTypeListSerializer(many=True)

    class Meta:
        model = GradeTypeGroup
        fields = ['id', 'name', 'types']


class GradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "name",
            "price",
            "level"
        )


class CourseReviewSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    helped = serializers.SerializerMethodField()
    not_helped = serializers.SerializerMethodField()

    class Meta:
        model = CourseReview
        exclude = ['course']

    def get_helped(self, obj):
        return obj.helped.count()

    def get_not_helped(self, obj):
        return obj.not_helped.count()


class CourseReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReview
        fields = ['rating', 'advantages', 'disadvantages', 'comment']


class CourseRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    club_name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'start_time', 'duration', 'course_name', 'club_name', 'address', 'regular_clients',
                  'regular_places', 'uniclass_clients', 'uniclass_places', 'unipass_clients', 'unipass_places',
                  'is_favorite', 'rating']

    def get_duration(self, obj):
        return obj.course.lesson_duration

    def get_course_name(self, obj):
        return obj.course.name

    def get_club_name(self, obj):
        return obj.course.grade.club.name

    def get_address(self, obj):
        return obj.course.grade.club.address

    def get_is_favorite(self, obj):
        if not self.context.get('user'):
            return None
        return obj.favorite_users.filter(id=self.context.get('user')).exists()

    def get_rating(self, obj):
        count = CourseReview.objects.filter(course=obj.course).count()
        if count == 0:
            return 0
        sum = 0
        for review in CourseReview.objects.filter(course=obj.course):
            sum += review.rating
        return sum / count


class LessonRetrieveSerializer(LessonSerializer):
    coaches = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()
    club = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()

    class Meta(LessonSerializer.Meta):
        fields = LessonSerializer.Meta.fields + ['coaches', 'rating', 'review', 'club', 'course']

    def get_coaches(self, obj):
        serializer = CoachClubSerializer(obj.course.coaches, many=True)
        return serializer.data

    def get_rating(self, obj):
        count = CourseReview.objects.filter(course=obj.course).count()
        if count == 0:
            return 0
        sum = 0
        for review in CourseReview.objects.filter(course=obj.course):
            sum += review.rating
        return sum / count

    def get_review(self, obj):
        review = CourseReview.objects.filter(course=obj.course).order_by('-created_at').first()
        if review:
            serializer = CourseReviewSerializer(review)
            return serializer.data
        return review

    def get_club(self, obj):
        serializer = ClubRetrieveSerializer(obj.course.grade.club)
        return serializer.data

    def get_course(self, obj):
        serializer = CourseRetrieveSerializer(obj.course)
        return serializer.data


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        exclude = "club",

    def validate(self, data):
        if data.get('from_age') < 1 or data.get('from_age') > 18 or data.get('to_age') < 1 or data.get('to_age') > 18:
            raise serializers.ValidationError("Диапозон возраста: 1 - 18")
        if data.get('from_age') > data.get('to_age'):
            raise serializers.ValidationError("Возраст от должен быть меньше чем возраст до")
        return data


class LessonDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonDay
        exclude = "course",


class CourseSerializer(serializers.ModelSerializer):
    lesson_days = LessonDaySerializer(many=True)

    class Meta:
        model = Course
        exclude = "grade",

    @transaction.atomic
    def create(self, validated_data):
        lesson_days = validated_data.pop("lesson_days")
        course = super().create(validated_data)

        for lesson_day in lesson_days:
            LessonDay.objects.create(
                course=course,
                weekday=lesson_day["weekday"],
                start_time=lesson_day["start_time"],
                end_time=lesson_day["end_time"]
            )

        Lesson.generate_lessons_for_course(course=course)

        return course


class CourseReviewHelpedSerializer(serializers.ModelSerializer):
    helped = serializers.BooleanField(required=True)

    class Meta:
        model = CourseReview
        fields = ['helped']

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        if validated_data.get('helped'):
            if instance.helped.filter(id=user.id).exists():
                instance.helped.remove(user)
            else:
                instance.helped.add(user)
                instance.not_helped.remove(user)
        else:
            if instance.not_helped.filter(id=user.id).exists():
                instance.not_helped.remove(user)
            else:
                instance.not_helped.add(user)
                instance.helped.remove(user)
        instance.save()
        return instance


class AttendanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceType
        fields = '__all__'


class LessonScheduleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'start_time', 'end_time', 'status']

    def get_name(self, obj):
        return obj.course.name

    def get_status(self, obj):
        try:
            status = LessonUserStatus.objects.get(lesson=obj, user=self.context.get('user'))
            return general.get_value_from_choices(constants.LESSON_STATUSES, status)
        except:
            return None


class LessonUserStatusCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonUserStatus
        fields = ['status']
