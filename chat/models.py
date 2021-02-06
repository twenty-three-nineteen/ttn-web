from django.db import models

from account.models import User, OpeningMessage
from ood_project.models import Chat, TextMessage, ChatUserInfo, Message


class MyMessage(TextMessage):

    class Meta:
        db_table = "messages"


class MyChat(Chat):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    opening_message = models.ForeignKey(to=OpeningMessage, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, default=ACTIVE)

    class Meta:
        db_table = "chats"


class MyChatUserInfo(ChatUserInfo):

    class Meta:
        db_table = "chat_user_infos"
