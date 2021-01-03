import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.authtoken.models import Token

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe

from account.models import User
from .models import Chat


class NotificationManager:
    def send_join_notification(self, username, chatId, participants):
        self.send_notification('join_the_group', username, chatId, participants)

    def send_leave_notification(self, username, chatId, participants):
        self.send_notification('left_the_group', username, chatId, participants)

    def send_notification(self, command, username, chatId, participants):
        content = {
            'command': command,
            'message': {
                'username': username,
                'chatId': chatId
            }
        }
        channel_layer = get_channel_layer()
        for participant in participants:
            participant_group_name = participant.username
            async_to_sync(channel_layer.group_send)(
                participant_group_name,
                {
                    'type': 'chat_message',
                    'message': content
                }
            )


def check_user_chat_access(user, chatId):
    chat = get_object_or_404(Chat, id=chatId)
    if not (user in chat.participants.all()):
        raise PermissionDenied('You do not have access to this chat.')
    if chat.status == Chat.INACTIVE:
        raise PermissionDenied('This chat is inactive.')


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-send_date').all()[:10:-1]


def get_user(username):
    return get_object_or_404(User, username=username)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)


@login_required
def room(request, chatId):
    token = get_object_or_404(Token, user=request.user)
    return render(request, 'chat/room.html', {
        'username': mark_safe(json.dumps(request.user.username)),
        'token': mark_safe(json.dumps(token.key)),
        'chatId': mark_safe(mark_safe(json.dumps(chatId))),
    })
