from django.db import transaction
from rest_framework import serializers

from .models import Grade, Course, LessonDay, Lesson, GradeType


class GradeTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeType
        fields = '__all__'


class GradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "name",
            "price",
            "level"
        )


class LessonSerializer(serializers.ModelSerializer):
    course = GradeListSerializer()

    class Meta:
        model = Lesson
        fields = "__all__"


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
