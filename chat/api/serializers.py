from rest_framework import serializers

from account.models import User
from chat.models import MyChat


class ParticipantSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(source='profile.avatar.id', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'name', 'avatar')


class ChatSerializer(serializers.ModelSerializer):
    opening_message = serializers.CharField(source='opening_message.message', read_only=True)

    class Meta:
        model = MyChat
        fields = ('id', 'opening_message', 'created_date')
