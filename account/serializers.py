from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import *


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password')


class OpeningMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningMessage
        fields = ["id", "owner", "message"]