from django.db import models

from account.models import User


class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username


class Chat(models.Model):
    participants = models.ManyToManyField(
        User, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)
