from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.models import Chat
from .serializers import ChatSerializer
from ..views import NotificationManager

User = get_user_model()


class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.all().filter(participants=self.request.user).exclude(status=Chat.INACTIVE)

    @action(methods=['delete'], detail=True)
    def left(self, request, pk):
        chat = self.get_queryset().get(id=pk)
        chat.participants.remove(request.user)
        if len(chat.participants.all()) < 2:
            chat.status = Chat.INACTIVE
        chat.save()
        NotificationManager().send_leave_notification(request.user.username, chat.id, chat.participants.all())
        return Response({'msg': 'left successfully'}, status=status.HTTP_200_OK)
