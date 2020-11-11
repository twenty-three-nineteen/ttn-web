from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from .permissions import *
from .serializers import *
from .models import OpeningMessage


class OpeningMessageViewSet(viewsets.ModelViewSet):
    serializer_class = OpeningMessageSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        return OpeningMessage.objects.all().filter(owner=self.request.user)


class ExploreViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return OpeningMessage.objects.all().exclude(owner=self.request.user).exclude(viewed_by_users=self.request.user)

    @action(detail=False, methods=['get'])
    def get_suggested_opening_message(self, request):
        opening_message_to_show = self.get_suggested_for_user()
        opening_message_to_show.viewed_by_users.add(request.user)
        return JsonResponse(OpeningMessageSerializer(opening_message_to_show).data, safe=False)

    def get_suggested_for_user(self):
        opening_messages = self.get_queryset()
        if len(opening_messages) == 0:
            raise FileNotFoundError('No opening message to show')
        return opening_messages[0]
