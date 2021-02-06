from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.models import MyChat, MyChatUserInfo
from .serializers import ChatSerializer, ParticipantSerializer
from ..managers import NotificationManager, MyChatManager

User = get_user_model()


class MCUIViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MyChatUserInfo.objects.all().filter(user=self.request.user).exclude(chat__status=MyChat.INACTIVE)

    @action(methods=['get'], detail=False)
    def list(self, request):
        mcuis = self.get_queryset()
        chats = [mcui.chat for mcui in mcuis]
        return JsonResponse(ChatSerializer(chats, many=True).data, safe=False)

    @action(methods=['get'], detail=True)
    def retrieve(self, request, pk):
        chat_mgr = MyChatManager(pk)
        return JsonResponse(ParticipantSerializer(chat_mgr.get_participants(), many=True).data, safe=False)

    @action(methods=['delete'], detail=True)
    def left(self, request, pk):
        chat_mgr = MyChatManager(pk)
        chat_mgr.left_the_chat(self.request.user)
        NotificationManager().send_leave_notification(request.user.username, chat_mgr.chat.id, chat_mgr.get_participants())
        return Response({'msg': 'left successfully'}, status=status.HTTP_200_OK)
