import random

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator

from chat.consumers import get_user_chat_consumer
from chat.managers import NotificationManager, MyChatManager
from .permissions import *
from .serializers import *
from .models import *
from chat.models import MyChat


class UserProfileViewSet(viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
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
        return OpeningMessage.objects.all()

    def perform_create(self, serializer):
        opening_message = serializer.save(owner=self.request.user)
        chat = MyChat.objects.create(opening_message=opening_message)
        chat_mgr = MyChatManager(chat.id)
        chat_mgr.join_the_chat(self.request.user)
        chat_mgr.create_text_message(author=self.request.user, text=opening_message.message)

    def list(self, request, *args, **kwargs):
        page_num = kwargs.get('page')
        username = kwargs.get('username')
        my_posts = self.get_queryset().filter(owner__username=username).order_by('-id')
        paginator = Paginator(my_posts, 8)
        if paginator.num_pages < page_num:
            return Response({'msg': 'finished'}, status=status.HTTP_404_NOT_FOUND)
        next_three_posts = paginator.get_page(page_num)
        return JsonResponse(OpeningMessageSerializer(next_three_posts, many=True).data, safe=False)


class ExploreViewSet(viewsets.GenericViewSet):
    serializer_class = ExploreSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = OpeningMessage.objects.all()
        queryset = queryset.filter(status=OpeningMessage.ACTIVE)
        queryset = queryset.exclude(owner=self.request.user)
        queryset = queryset.exclude(viewed_by_users=self.request.user)
        
        if 'max_number_of_members' in self.request.data:
            queryset = queryset.filter(max_number_of_members=self.request.data['max_number_of_members'])

        if 'categories' in self.request.data:
            for cat in self.request.data['categories']:
                queryset = queryset.filter(categories=cat)

        return queryset

    @action(detail=False, methods=['post'])
    def get_suggested_opening_message(self, request):
        opening_message_to_show = self.get_suggested_for_user()
        if opening_message_to_show is None:
            return Response({'msg': 'No opening message to show'}, status=status.HTTP_404_NOT_FOUND)
        opening_message_to_show.viewed_by_users.add(request.user)
        return JsonResponse(OpeningMessageSerializer(opening_message_to_show).data, safe=False)

    def get_suggested_for_user(self):
        opening_messages = self.get_queryset()
        if len(opening_messages) == 0:
            return None
        return random.choice(opening_messages)


class RequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, RequestPermission, ]
    serializer_class = RequestSerializer

    def get_queryset(self):
        return RequestModel.objects.all().filter(target=self.request.user, state=RequestModel.PENDING)

    def perform_create(self, serializer):
        serializer.save(source=self.request.user, target=serializer.validated_data['opening_message'].owner)

    @action(detail=False, methods=['put'])
    def accept_request(self, request, pk):
        try:
            chatRequest = self.get_queryset().get(id=pk)
            chatRequest.state = RequestModel.ACCEPTED
            chatRequest.save()
            opening_message = chatRequest.opening_message
            chats = MyChat.objects.all().filter(opening_message=opening_message).filter(status=MyChat.ACTIVE)
            chat_mgr = None
            for chat in chats:
                if len(MyChatManager(chat.id).get_participants()) < opening_message.max_number_of_members:
                    chat_mgr = MyChatManager(chat.id)
            chat_mgr.join_the_chat(chatRequest.source)
            NotificationManager().send_join_notification(chatRequest.source.username,
                                                         chat_mgr.chat.id,
                                                         chat_mgr.get_participants())
            get_user_chat_consumer(chatRequest.source).create_new_message(chatRequest.message, chat_mgr.chat.id)
            if len(chat_mgr.get_participants()) == opening_message.max_number_of_members \
                    and opening_message.max_number_of_members > 2:
                opening_message.status = OpeningMessage.INACTIVE
                other_chat_requests = self.get_queryset().filter(opening_message=opening_message)
                for r in list(other_chat_requests):
                    r.state = RequestModel.REJECTED
                    r.save()
            elif opening_message.max_number_of_members == 2:
                newChat = MyChat.objects.create(opening_message=opening_message)
                new_chat_mgr = MyChatManager(newChat.id)
                new_chat_mgr.join_the_chat(request.user)
                new_chat_mgr.create_text_message(author=request.user, text=opening_message.message)

        except RequestModel.DoesNotExist:
            return Response({'msg': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': 'accepted successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'])
    def reject_request(self, request, pk):
        try:
            self.get_queryset().filter(id=pk).update(state=RequestModel.REJECTED)
        except RequestModel.DoesNotExist:
            return Response({'msg': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': 'rejected successfully'}, status=status.HTTP_200_OK)


class InterestsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = InterestSerializer

    def get_queryset(self):
        return Interest.objects.all()

    def search(self, request, *args, **kwargs):
        searched_text = kwargs.get('searched_text').lower()
        if len(searched_text) == 0:
            Response({'msg': 'Type something!'}, status=status.HTTP_404_NOT_FOUND)
        searched_list = self.get_queryset().filter(subject__startswith=searched_text)
        return JsonResponse(self.serializer_class(searched_list, many=True).data, safe=False)
