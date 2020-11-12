from django.http import JsonResponse
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import *
from .serializers import *
from .models import *


# @api_view(['GET'])
# @permission_classes([UserPermission, IsAuthenticated])
# def get_user_profile_username(request, username):
#     try:
#         curr_user = User.objects.get(username=username)
#         curr_user_profile = UserProfile.objects.get(user_id=curr_user.id)
#     except UserProfile.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         return Response(
#             {
#                 "user": (UserCreateSerializer(curr_user)).data,
#                 "user_profile": (UserProfileSerializer(curr_user_profile)).data
#             }
#         )


# @api_view(['PUT'])
# @permission_classes([UserPermission, IsAuthenticated])
# def update_user_profile(request, username):
#     try:
#         curr_user = User.objects.get(username=username)
#         curr_user_profile = UserProfile.objects.get(user_id=curr_user.id)
#     except UserProfile.DoesNotExist:
#         return Response(status=status.HTTP_403_FORBIDDEN)
#     if request.method == 'PUT':
#         serializer = UserProfileSerializer(curr_user_profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {
#                     "success": "update successfully",
#                     "code": 1
#                 }, status=status.HTTP_200_OK
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
