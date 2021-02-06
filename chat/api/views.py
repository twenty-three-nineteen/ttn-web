from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.models import MyChat
from .serializers import ChatSerializer, ParticipantSerializer
from ..managers import NotificationManager, MyChatManager

User = get_user_model()


class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MyChat.objects.all().filter(participants=self.request.user).exclude(status=MyChat.INACTIVE)

    @action(methods=['delete'], detail=True)
    def left(self, request, pk):
        chat = self.get_queryset().get(id=pk)
        chat.participants.remove(request.user)
        if len(chat.participants.all()) < 2:
            chat.status = MyChat.INACTIVE
        chat.save()
        NotificationManager().send_leave_notification(request.user.username, chat.id, chat.participants.all())
        return Response({'msg': 'left successfully'}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def get_participants(self, request, pk):
        chat_mgr = MyChatManager(pk)
        participants = chat_mgr.get_participants()
        ParticipantSerializer(participants, many=True)
        return JsonResponse(ParticipantSerializer(participants, many=True).data, safe=False)
