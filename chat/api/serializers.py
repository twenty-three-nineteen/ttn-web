from rest_framework import serializers

from account.models import User
from chat.models import Chat


class ParticipantSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(source='profile.avatar.id', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'name', 'avatar')


class ChatSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    opening_message = serializers.CharField(source='opening_message.message', read_only=True)

    class Meta:
        model = Chat
        fields = ('id', 'participants', 'opening_message', 'created_date')
