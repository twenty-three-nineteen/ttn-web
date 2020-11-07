from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from account import serializers

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
