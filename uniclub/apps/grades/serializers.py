from django.db import transaction
from rest_framework import serializers

from .models import Grade, Course, LessonDay, Lesson


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        exclude = "club",


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
