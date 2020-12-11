from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import *
from .serializers import *
from .models import *
from chat.models import Chat, Message


class UserProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, UserPermission, ]

    @action(methods=['get'], detail=True)
    def get_user_profile(self, request, username):
        curr_user = get_object_or_404(User, username=username)
        curr_user_profile = get_object_or_404(UserProfile, user=curr_user)
        return JsonResponse(UserProfileSerializer(curr_user_profile).data, safe=False)

    @action(methods=['put'], detail=True)
    def update_user_profile(self, request, username):
        curr_user = get_object_or_404(User, username=username)
        curr_user_profile = get_object_or_404(UserProfile, user=curr_user)
        # TOF
        if 'name' in request.data and request.data['name'] is not None:
            curr_user.name = request.data['name']
            curr_user.save()
        serializer = UserProfileSerializer(curr_user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'update successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OpeningMessageViewSet(viewsets.ModelViewSet):
    serializer_class = OpeningMessageSerializer
    permission_classes = [IsAuthenticated, IsOwner]

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
            return Response({'msg': 'No opening message to show'}, status=status.HTTP_404_NOT_FOUND)
        return opening_messages[0]


class RequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, RequestPermission, ]
    serializer_class = RequestSerializer

    def get_queryset(self):
        return RequestModel.objects.all().filter(target=self.request.user, state='pending')

    @action(detail=False, methods=['put'])
    def accept_request(self, request, pk):
        try:
            chatRequest = self.get_queryset().get(id=pk)
            chatRequest.state = 'accepted'
            chatRequest.save()
            chat = Chat.objects.create()
            chat.participants.add(chatRequest.source, chatRequest.target)
            chat.messages.add(Message.objects.create(author=chatRequest.target,
                                                     content=chatRequest.opening_message.message),
                              Message.objects.create(author=chatRequest.source,
                                                     content=chatRequest.message))
            chat.save()
        except RequestModel.DoesNotExist:
            return Response({'msg': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': 'accepted successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'])
    def reject_request(self, request, pk):
        try:
            self.get_queryset().filter(id=pk).update(state='rejected')
        except RequestModel.DoesNotExist:
            return Response({'msg': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': 'rejected successfully'}, status=status.HTTP_200_OK)


class InterestsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = InterestSerializer

    def get_queryset(self):
        return Interest.objects.all()
