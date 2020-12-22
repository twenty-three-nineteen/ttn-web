from datetime import datetime

from django.db import models

from account.models import User, OpeningMessage


class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    class Meta:
        db_table = "messages"


class Chat(models.Model):

    WAITING = 'waiting_for_members'
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    opening_message = models.ForeignKey(to=OpeningMessage, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, default=ACTIVE)
    participants = models.ManyToManyField(User, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chats"
