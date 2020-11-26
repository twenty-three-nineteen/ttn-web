import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe

from account.models import User
from .models import Chat


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-send_date').all()[:10:-1]


def get_user(username):
    return get_object_or_404(User, username=username)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)


def index(request):
    return render(request, 'chat/index.html', {})


@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })
