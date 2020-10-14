from rest_framework import serializers
from apps.users.models import User
from apps.person.models import ClientProfile


class ClientProfileCreateSerializer(serializers.ModelSerializer):



class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = []