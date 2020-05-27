from rest_framework import serializers

from .models import Grade, Lesson


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        exclude = "club",


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        exclude = "grade",
