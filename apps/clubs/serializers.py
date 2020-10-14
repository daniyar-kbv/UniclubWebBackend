from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from .models import Club, ClubImage, ClubReview
from apps.users.serializers import UserShortSerializer
from apps.grades.serializers import GradeTypeListSerializer
from apps.grades.models import GradeType
from apps.person.serializers import CoachClubSerializer


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
    grades = serializers.SerializerMethodField()
    coaches = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = ["id", "images", "address", "latitude", "longitude", "instagram", "facebook", "vk", "mobile_phone",
                  "home_phone", "work_phone", "email", "website", "image", "short_description", "description",
                  "competition_frequency", "hazard_information", "student_achievements", "events_information",
                  "other_services", "parking_available", "places_for_parents", "parent_presence", "video_monitoring",
                  "classes_for_disabled", "floor_area", "number_of_bathrooms", "number_of_changing_rooms",
                  "total_number_of_students", "social_reviews", "from_age", "to_age", "is_new", "name", "city",
                  "club_admin", "grades", "coaches", "reviews"]

    def get_grades(self, obj):
        grades = GradeType.objects.filter(grades__club=obj)
        serializer = GradeTypeListSerializer(grades, many=True)
        return serializer.data

    def get_coaches(self, obj):
        coaches = obj.coaches
        serializer = CoachClubSerializer(coaches, many=True)
        return serializer.data

    def get_reviews(self, obj):
        reviews = obj.reviews
        serializer = ClubReviewSerializer(reviews, many=True)
        return serializer.data


class ClubListSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()

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
        )

    def get_is_favorite(self, obj):
        if not self.context.get('user'):
            return None
        return obj.favorite_users.filter(id=self.context.get('user')).exists()


class ClubForFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = (
            "id",
            "name",
        )


class ClubUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        exclude = "club_admin",

    def validate(self, data):
        if data.get('from_age') < 1 or data.get('from_age') > 18 or data.get('to_age') < 1 or data.get('to_age') > 18:
            raise serializers.ValidationError("Диапозон возраста: 1 - 18")
        if data.get('from_age') > data.get('to_age'):
            raise serializers.ValidationError("Возраст от должен быть меньше чем возраст до")
        return data
