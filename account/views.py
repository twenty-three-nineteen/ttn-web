from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from account import serializers
from . import models, permissions

from account.models import OpeningMessage


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def restricted(request):
    return Response(data="Only for Logged in User", status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def next_opening_message(request):
    opening_messages = OpeningMessage.objects.all().exclude(user=request.user).exclude(viewed_by_users=request.user)
    if len(opening_messages) == 0:
        raise FileNotFoundError('No opening message to show')
    opening_message_to_show = opening_messages[0]
    opening_message_to_show.viewed_by_users.add(request.user)
    return JsonResponse(serializers.OpeningMessageForExplore(opening_message_to_show).data, safe=False)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, permissions.UserPermission, ])
def get_user_profile_username(request, username):
    try:
        curr_user = models.User.objects.get(username=username)
        curr_user_profile = models.UserProfile.objects.get(user_id=curr_user.id)
    except models.UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return Response(
            {
                "user": (serializers.UserSerializer(curr_user)).data,
                "user_profile": (serializers.UserProfileSerializer(curr_user_profile)).data
            }
        )


@api_view(['PUT'])
@permission_classes([permissions.UserPermission])
def update_user_profile(request, username):
    try:
        curr_user = models.User.objects.get(username=username)
        curr_user_profile = models.UserProfile.objects.get(user_id=curr_user.id)
    except models.UserProfile.DoesNotExist:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == 'PUT':
        serializer = serializers.UserProfileSerializer(curr_user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": "update successfully",
                    "code": 1
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
