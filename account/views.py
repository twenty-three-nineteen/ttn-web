from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator

from .permissions import *
from .serializers import *
from .models import *


class UserProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, UserPermission, ]

    @action(methods=['get'], detail=False)
    def get_user_profile_username(self, request, username):
        curr_user = get_object_or_404(User, username=username)
        curr_user_profile = get_object_or_404(UserProfile, user=curr_user)
        return JsonResponse(UserProfileSerializer(curr_user_profile).data, safe=False)

    @action(methods=['put'], detail=False)
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
            return Response(
                {
                    "success": "update successfully",
                    "code": 1
                }, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OpeningMessageViewSet(viewsets.ModelViewSet):
    serializer_class = OpeningMessageSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return OpeningMessage.objects.all().filter(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        page_num = request.data.get('page')
        my_posts = self.get_queryset()
        paginator = Paginator(my_posts, 8)
        if paginator.num_pages < page_num:
            return Response({'msg': 'finished'}, status=status.HTTP_404_NOT_FOUND)
        next_three_posts = paginator.get_page(page_num)
        return JsonResponse(OpeningMessageSerializer(next_three_posts, many=True).data, safe=False)


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


class RequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, RequestPermission, ]
    serializer_class = RequestSerializer

    def get_queryset(self):
        queryset = RequestModel.objects.all().filter(target=self.request.user, state='pending')
        return queryset

    @action(detail=False, methods=['put'])
    def accept_request(self, request, pk):
        try:
            RequestModel.objects.filter(id=pk).update(state='accepted')
        except RequestModel.DoesNotExist:
            return Response({'msg': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': 'accepted successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'])
    def reject_request(self, request, pk):
        try:
            RequestModel.objects.filter(id=pk).update(state='rejected')
        except RequestModel.DoesNotExist:
            return Response({'msg': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': 'rejected successfully'}, status=status.HTTP_200_OK)


class InterestsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = InterestSerializer

    def get_queryset(self):
        queryset = Interest.objects.all()
        return queryset
