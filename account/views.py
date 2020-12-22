import operator
import random
from functools import reduce

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        opening_message = serializer.save()
        chat = Chat.objects.create(opening_message=opening_message)
        chat.participants.add(request.user)
        chat.messages.add(Message.objects.create(author=request.user, content=opening_message.message))
        chat.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        page_num = request.data.get('page')
        my_posts = self.get_queryset()
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
        queryset = queryset.exclude(owner=self.request.user)
        queryset = queryset.exclude(viewed_by_users=self.request.user)

        if 'max_number_of_members' in self.request.data:
            queryset = queryset.filter(numberOfMembers=self.request.data['max_number_of_members'])

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

    @action(detail=False, methods=['put'])
    def accept_request(self, request, pk):
        try:
            chatRequest = self.get_queryset().get(id=pk)
            chatRequest.state = RequestModel.ACCEPTED
            chatRequest.save()
            chat = Chat.objects.all().filter(opening_message=chatRequest.opening_message)\
                .filter(status=Chat.WAITING)[0]
            chat.participants.add(chatRequest.source)
            chat.messages.add(Message.objects.create(author=chatRequest.source,
                                                     content=chatRequest.message))
            if len(chat.participants.all()) == chatRequest.opening_message.max_number_of_members:
                chat.status = Chat.ACTIVE
                other_chat_requests = self.get_queryset()
                for r in list(other_chat_requests):
                    if r.state == RequestModel.PENDING:
                        r.state = RequestModel.REJECTED
                    r.save()
            chat.save()

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
