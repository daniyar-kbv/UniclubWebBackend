from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import (
    ClientProfile, ClientChildren
)
from apps.grades.models import Coach, LessonUserStatus, Lesson
from apps.grades.serializers import LessonScheduleSerializer

import constants, datetime

User = get_user_model()


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        exclude = "club",


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = (
            "sex",
            "city",
            "birth_date",
            "image"
        )


class ClientProfileUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "profile",
        )

    def update(self, instance, validated_data):
        if validated_data.get("profile"):
            profile_data = validated_data.pop("profile")
            profile_serializer = ProfileUpdateSerializer(instance=instance.profile, data=profile_data)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()

        instance.save()
        return super().update(instance, validated_data)


class ClientChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientChildren
        fields = "__all__"
        extra_kwargs = {
            "parent": {"required": False}
        }


class ScheduleSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        user = self.context.get('user')
        lessons = Lesson.objects.filter(
            Q(
                Q(regular_users=user) | Q(uniclass_users=user) | Q(unipass_users=user)
            ) & Q(day=instance)
        ).order_by('start_time')
        lessons_serializer = LessonScheduleSerializer(lessons, many=True, context=self.context)
        return {
            'date': instance.strftime(constants.DATE_FORMAT),
            'weekday': instance.weekday(),
            'lessons': lessons_serializer.data
        }
