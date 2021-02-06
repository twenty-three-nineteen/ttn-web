from django.db import models

from account.models import User, OpeningMessage
from ood_project.models import Chat, TextMessage, ChatUserInfo, Message


class MyMessage(TextMessage):

    author = models.ForeignKey('MyChatUserInfo', related_name='author_messages', on_delete=models.CASCADE)
    replied_message = models.ForeignKey('MyMessage', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "messages"


class MyChat(Chat):

    ACTIVE = 'active'
    INACTIVE = 'inactive'

    opening_message = models.ForeignKey(to=OpeningMessage, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, default=ACTIVE)
    messages = models.ManyToManyField(MyMessage, blank=True)

    class Meta:
        db_table = "chats"


class MyChatUserInfo(ChatUserInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(MyChat, on_delete=models.CASCADE)

    class Meta:
        db_table = "chat_user_infos"
