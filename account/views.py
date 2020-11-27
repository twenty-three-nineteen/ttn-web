from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import *
from .serializers import *
from .models import *


class UserProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, UserPermission, ]

    @action(methods=['get'], detail=False)
    def get_user_profile_username(self, request, username):
        try:
            curr_user = User.objects.get(username=username)
            curr_user_profile = UserProfile.objects.get(user_id=curr_user.id)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            return Response(
                {
                    "user": (UserCreateSerializer(curr_user)).data,
                    "user_profile": (UserProfileSerializer(curr_user_profile)).data
                }
            )

    @action(methods=['put'], detail=False)
    def update_user_profile(self, request, username):
        try:
            curr_user = User.objects.get(username=username)
            curr_user_profile = UserProfile.objects.get(user_id=curr_user.id)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if request.method == 'PUT':
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
    def response_request(self, request, state):
        source = request.data['source']
        target = request.data['target']
        opening_message = request.data['opening_message']
        updated_state = request.data['state']
        if state != 'accepted' and state != 'rejected':
            return Response({'msg': f'{state} not allowed in url'}, status=status.HTTP_400_BAD_REQUEST)
        if (updated_state is None) or (updated_state != state):
            return Response({'msg': f'{state} is not match with {updated_state}'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            curr_request = RequestModel.objects.get(source=source, opening_message=opening_message, target=target)
        except RequestModel.DoesNotExist:
            return Response({'msg': 'not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RequestSerializer(curr_request, data=request.data)
        if not serializer.is_valid():
            return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': f'{state} successfully'}, status=status.HTTP_200_OK)
