from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.models import Chat
from .serializers import ChatSerializer

User = get_user_model()


class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.all().filter(participants=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     participants = request.data['participants']
    #     chat = Chat()
    #     chat.save()
    #     for username in participants:
    #         user = User.objects.get(username=username)
    #         chat.participants.add(user)
    #     chat.save()
    #     return Response({'msg': 'created successfully'}, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=True)
    def left(self, request, pk):
        chat = self.get_queryset().get(id=pk)
        chat.participants.remove(request.user)
        if len(chat.participants.all()) < 2:
            chat.delete()
        chat.save()
        return Response({'msg': 'left successfully'}, status=status.HTTP_200_OK)
