from rest_framework import serializers
from apps.users.models import User
from apps.person.models import ClientProfile
from apps.clubs.models import Club, ClubReview, ClubImage
from apps.grades.models import Course, LessonDay, Lesson, CourseReview, Coach


class ClientProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = '__all__'
        read_only_fields = ['user']


class ClientCreateSerializer(serializers.ModelSerializer):
    profile = ClientProfileCreateSerializer()

    class Meta:
        model = User
        fields = ["password", "first_name", "last_name", "middle_name", "mobile_phone", "email", "user_type", "profile"]

    def create(self, validated_data):
        password = validated_data.get('password')
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        profile = user.profile
        profile.delete()
        profile_data['user'] = user
        ClientProfile.objects.create(**profile_data)
        return user


class ClubCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'


class ClubImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubImage
        fields = ['image']


class PartnerCreateSerializer(serializers.ModelSerializer):
    club = ClubCreateSerializer()

    class Meta:
        model = User
        fields = ["password", "first_name", "last_name", "middle_name", "mobile_phone", "email", "user_type", "club"]

    def create(self, validated_data):
        password = validated_data.get('password')
        club_data = validated_data.pop('club')
        images = self.context.get('images')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        profile = user.club
        profile.delete()
        club_data['user'] = user
        club_data["city"] = club_data["city"].id
        club_serializer = ClubCreateSerializer(data=club_data)
        club_serializer.is_valid(raise_exception=True)
        club = club_serializer.save()
        for image in images:
            d = {
                'image': image
            }
            serializer = ClubImageCreateSerializer(data=d)
            serializer.is_valid(raise_exception=True)
            serializer.save(club=club)
        return user


class CoachCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        exclude = ['club']

    def create(self, validated_data):
        coach = Coach.objects.create(**validated_data, club=validated_data.get('course').grade.club)
        return coach


class LessonDayCreateSerializer(serializers.ModelSerializer):
    course = serializers.IntegerField(required=False)

    class Meta:
        model = LessonDay
        fields = '__all__'


class CourseCreateSerializer(serializers.ModelSerializer):
    lesson_days = serializers.ListField(child=LessonDayCreateSerializer(), write_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        extra_fields = ['lesson_days']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CourseCreateSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    def create(self, validated_data):
        lesson_days_data = validated_data.pop('lesson_days')
        course = Course.objects.create(**validated_data)
        for lesson_day_data in lesson_days_data:
            lesson_day_data['course'] = course
            LessonDay.objects.create(**lesson_day_data)
        Lesson.generate_lessons_for_course(course=course)
        return course


class ClubReviewCreateSerializerTest(serializers.ModelSerializer):
    class Meta:
        model = ClubReview
        fields = '__all__'


class CourseReviewCreateSerializerTest(serializers.ModelSerializer):
    class Meta:
        model = CourseReview
        fields = '__all__'
