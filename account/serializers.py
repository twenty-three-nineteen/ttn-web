from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import *


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'name')


class OpeningMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningMessage
        fields = ["id", "owner", "message"]


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'name', 'bio', 'birthday', 'avatar', 'interests']


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['subject']


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['name']


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestModel
        fields = ['id', 'source', 'target', 'opening_message', 'state', 'message']
