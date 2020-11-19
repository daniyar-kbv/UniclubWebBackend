from datetime import date, timedelta

from rest_framework import serializers
from django.db.transaction import atomic
from django.db.models import Count, Q
from dateutil.relativedelta import relativedelta

from apps.users.models import User
from apps.person.serializers import ClientChildrenSerializer, ClientChildrenShortSerializer
from apps.clubs.serializers import ClubForFilterSerializer
from apps.grades.serializers import CourseShortSerializer
from apps.grades.models import Course
from apps.products.models import Product

from .import SubscriptionOperations
from .models import Subscription, FreezeRequest, LessonBooking

import datetime, constants


class FreezeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreezeRequest
        fields = "__all__"


class SubscriptionListSerializer(serializers.ModelSerializer):
    child = ClientChildrenSerializer()

    class Meta:
        model = Subscription
        fields = "__all__"


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "customer": {"read_only": True},
            "start_date": {"read_only": True},
            "end_date": {"read_only": True}
        }

    def validate(self, attrs):
        request = self.context["request"]
        client_profile = request.user.profile

        if not client_profile == attrs["child"].parent:
            raise serializers.ValidationError("Invalid childId specified")

        return super().validate(attrs)

    @atomic
    def create(self, validated_data):
        request = self.context["request"]
        product: Product = validated_data["product"]
        child = validated_data["child"]
        start_date = date.today()

        subscription = Subscription.objects.create(
            customer=request.user,
            product=product,
            child=child,
            start_date=start_date,
            end_date=start_date + timedelta(days=product.days_amount)
        )

        subscription.add_history_record(operation=SubscriptionOperations.NEW)

        return subscription


class SubscriptionProfileSerializer(serializers.ModelSerializer):
    product_type = serializers.SerializerMethodField()
    time_left = serializers.SerializerMethodField()
    child = ClientChildrenSerializer()
    club = ClubForFilterSerializer()
    attended = serializers.SerializerMethodField()
    skipped = serializers.SerializerMethodField()
    attended_most = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ['id', 'product_type', 'time_left', 'child', 'status', 'club', 'attended', 'skipped', 'attended_most']

    def get_product_type(self, obj):
        return obj.product.product_type

    def get_time_left(self, obj):
        delta = relativedelta(obj.end_date, datetime.datetime.now())
        return {
            'months': delta.months,
            'days': delta.days,
            'hours': delta.hours
        }

    def get_attended(self, obj):
        return obj.bookings.filter(status=constants.LESSON_ATTENDED).count()

    def get_skipped(self, obj):
        return obj.bookings.filter(status=constants.LESSON_NOT_ATTENDED).count()

    def get_attended_most(self, obj):
        courses = Course.objects.all().annotate(attended=Count('lessons__bookings', filter=Q(lessons__bookings__user=obj.child)))
        course = courses.order_by('-attended').first() if courses.order_by('-attended').first().attended != 0 else None
        serializer = CourseShortSerializer(course)
        return serializer.data if courses.order_by('-attended').first().attended != 0 else None


class LessonBookingListSerializer(serializers.ModelSerializer):
    user = ClientChildrenShortSerializer()

    class Meta:
        model = LessonBooking
        fields = ['id', 'user', 'status']


class LessonBookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonBooking
        fields = ['status']


class LessonStatusesSerializer(serializers.ListSerializer):
    child = serializers.CharField()
