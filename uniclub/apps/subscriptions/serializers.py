from datetime import date, timedelta

from rest_framework import serializers
from django.db.transaction import atomic

from apps.users.models import User
from apps.person.serializers import ClientChildrenSerializer
from apps.products.models import Product

from .import SubscriptionOperations
from .models import Subscription


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
