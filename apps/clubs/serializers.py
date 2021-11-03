from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from rest_framework import serializers

from .models import Club, ClubImage, ClubReview
from apps.users.serializers import UserShortSerializer
from apps.users.models import User
from apps.grades.serializers import GradeTypeListSerializer, CoachClubSerializer
from apps.grades.models import GradeType, Coach, Lesson
from apps.person.models import ClientChildren, ClientProfile
from apps.subscriptions.models import LessonBooking, Subscription
from apps.subscriptions import SubscriptionStatuses
from apps.products.models import Product

from dateutil.relativedelta import relativedelta

import constants, datetime


class ClubReviewSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    helped = serializers.SerializerMethodField()
    not_helped = serializers.SerializerMethodField()

    class Meta:
        model = ClubReview
        exclude = ['club']

    def get_helped(self, obj):
        return obj.helped.count()

    def get_not_helped(self, obj):
        return obj.not_helped.count()


class ClubReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubReview
        fields = ['rating', 'advantages', 'disadvantages', 'comment']


class ClubImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubImage
        fields = "image",


class ClubRetrieveSerializer(serializers.ModelSerializer):
    images = ClubImageSerializer(many=True)
    grades = serializers.SerializerMethodField()
    coaches = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = ["id", "images", "address", "latitude", "longitude", "instagram", "facebook", "vk", "mobile_phone",
                  "home_phone", "work_phone", "email", "website", "image", "short_description", "description",
                  "competition_frequency", "hazard_information", "student_achievements", "events_information",
                  "other_services", "parking_available", "places_for_parents", "parent_presence", "video_monitoring",
                  "classes_for_disabled", "floor_area", "number_of_bathrooms", "number_of_changing_rooms",
                  "total_number_of_students", "social_reviews", "from_age", "to_age", "is_new", "name", "city",
                  "club_admin", "rating", "grades", "coaches", "review"]

    def get_grades(self, obj):
        grades = GradeType.objects.filter(courses__club=obj).distinct()
        serializer = GradeTypeListSerializer(grades, many=True)
        return serializer.data

    def get_coaches(self, obj):
        coaches = obj.coaches
        serializer = CoachClubSerializer(coaches, many=True)
        return serializer.data

    def get_review(self, obj):
        review = ClubReview.objects.filter(club=obj).order_by('-created_at').first()
        if review:
            serializer = ClubReviewSerializer(review)
            return serializer.data
        return review

    def get_rating(self, obj):
        count = ClubReview.objects.filter(club=obj).count()
        if count == 0:
            return 0
        sum = 0
        for review in ClubReview.objects.filter(club=obj):
            sum += review.rating
        return sum / count


class ClubListSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = (
            "id",
            "name",
            "short_description",
            "address",
            "longitude",
            "latitude",
            "image",
            "is_new",
            "is_favorite",
            "rating",
        )

    def get_is_favorite(self, obj):
        if not self.context.get('user'):
            return None
        return obj.favorite_users.filter(id=self.context.get('user')).exists()

    def get_rating(self, obj):
        count = ClubReview.objects.filter(club=obj).count()
        if count == 0:
            return 0
        sum = 0
        for review in ClubReview.objects.filter(club=obj):
            sum += review.rating
        return sum / count



class ClubForFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = (
            "id",
            "name",
        )


class ClubUpdateSerializer(serializers.ModelSerializer):
    coaches = CoachClubSerializer(many=True, read_only=True)

    class Meta:
        model = Club
        fields = '__all__'
        extra_fields = ['coaches']
        remove_fields = ['club_admin']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ClubUpdateSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            expanded_fields += self.Meta.extra_fields
        if getattr(self.Meta, 'remove_fields', None):
            for field in self.Meta.remove_fields:
                expanded_fields.remove(field)
        return expanded_fields

    def validate(self, data):
        if data.get('from_age') < 1 or data.get('from_age') > 18 or data.get('to_age') < 1 or data.get('to_age') > 18:
            raise serializers.ValidationError("Диапозон возраста: 1 - 18")
        if data.get('from_age') > data.get('to_age'):
            raise serializers.ValidationError("Возраст от должен быть меньше чем возраст до")
        return data


class ReviewHelpedSerializer(serializers.ModelSerializer):
    helped = serializers.BooleanField(required=True)

    class Meta:
        model = ClubReview
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


class ClubLessonScheduleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'start_time', 'end_time', 'unipass_clients', 'uniclass_clients', 'regular_clients',
                  'unipass_places', 'uniclass_places', 'regular_places']

    def get_name(self, obj):
        return obj.course.name


class ClubScheduleSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        club = self.context.get('club')
        lessons = Lesson.objects.filter(
            Q(course__club=club) & Q(day=instance)
        ).order_by('start_time')
        lessons_serializer = ClubLessonScheduleSerializer(lessons, many=True, context=self.context)
        return {
            'date': instance.strftime(constants.DATE_FORMAT),
            'weekday': instance.weekday(),
            'lessons': lessons_serializer.data
        }


class ClubScheduleCoachSerializer(serializers.ModelSerializer):
    grade_type = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Coach
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'grade_type', 'lessons']

    def get_grade_type(self, obj):
        return obj.grade_type.name if obj.grade_type else None

    def get_lessons(self, obj):
        club = self.context.get('club')
        date = self.context.get('date')
        lessons = Lesson.objects.filter(
            Q(course__club=club) & Q(day=date)
        ).order_by('start_time')
        lessons_serializer = ClubLessonScheduleSerializer(lessons, many=True, context=self.context)
        return lessons_serializer.data


class ProductClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'product_type']


class SubscriptionClubSerializer(serializers.ModelSerializer):
    product = ProductClubSerializer()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ['id', 'product', 'visits_amount', 'status']

    def get_status(self, obj):
        if relativedelta(datetime.date.today(), obj.end_date).weeks == 0 \
                and obj.status in [SubscriptionStatuses.ACTIVE, SubscriptionStatuses.FROZEN]:
            return 'EXPIRES_SOON'
        return obj.status


class UserClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'email', 'mobile_phone']


class ClientProfileClubSerializer(serializers.ModelSerializer):
    user = UserClubSerializer()

    class Meta:
        model = ClientProfile
        fields = ['id', 'image', 'user']


class ClubClientsSerializer(serializers.ModelSerializer):
    parent = ClientProfileClubSerializer()
    birth_date = serializers.DateTimeField(format=constants.DATE_FORMAT)
    visits_attended = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = ClientChildren
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'mobile_phone', 'email', 'birth_date', 'sex',
                  'parent', 'visits_attended', 'subscription']

    def get_visits_attended(self, obj):
        subscription = Subscription.objects.filter(child=obj).order_by('-created_at').first()
        return LessonBooking.objects.filter(
            user=obj, status=constants.LESSON_ATTENDED, subscription=subscription
        ).count()

    def get_subscription(self, obj):
        last_subscription = Subscription.objects.filter(child=obj).order_by('-created_at').first()
        serializer = SubscriptionClubSerializer(last_subscription)
        return serializer.data
