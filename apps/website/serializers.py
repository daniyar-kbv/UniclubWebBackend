from rest_framework import serializers

from .models import FeedBack, FAQ, PartnerFeedBack


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = "__all__"


class PartnerFeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerFeedBack
        fields = "__all__"
