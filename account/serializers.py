from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import *


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password')


class OpeningMessageForExplore(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = OpeningMessage
        fields = ["username", "message"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'birthday']


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['subject']
