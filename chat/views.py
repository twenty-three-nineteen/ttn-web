import json

from rest_framework.authtoken.models import Token

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe


@login_required
def room(request, chatId):
    token = get_object_or_404(Token, user=request.user)
    return render(request, 'chat/room.html', {
        'username': mark_safe(json.dumps(request.user.username)),
        'token': mark_safe(json.dumps(token.key)),
        'chatId': mark_safe(mark_safe(json.dumps(chatId))),
    })
