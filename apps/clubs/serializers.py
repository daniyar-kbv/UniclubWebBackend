from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from .models import Club, ClubImage, ClubReview
from apps.users.serializers import UserShortSerializer
from apps.grades.serializers import GradeTypeListSerializer, CoachClubSerializer
from apps.grades.models import GradeType


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
        grades = GradeType.objects.filter(courses__club=obj)
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
    class Meta:
        model = Club
        exclude = "club_admin",

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
