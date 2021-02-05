import enum

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=255, default=None, null=True)
    avatar = models.ImageField(upload_to='pictures/avatars/')


class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    send_date = models.DateTimeField(auto_now_add=True)


class ImageMessage(Message):
    image = models.ImageField(upload_to='pictures/messages/')


class TextMessage(Message):
    text = models.CharField()


class Chat(models.Model):
    messages = models.ManyToManyField(Message, blank=True)
    bio = models.CharField(max_length=255, default=None, null=True)
    avatar = models.ImageField(upload_to='pictures/chat_avatars/')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chats"


class MemberTypes(enum.Enum):
    MEMBER = 1
    ADMIN = 2
    OWNER = 3


class ChatUserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    cui_type = models.CharField(default=MemberTypes.MEMBER)
