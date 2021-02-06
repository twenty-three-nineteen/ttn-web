import enum

from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(models.Model):
    bio = models.CharField(max_length=255, default=None, null=True)
    avatar = models.ImageField(upload_to='pictures/avatars/')

    class Meta:
        abstract = True


class User(AbstractUser, Profile):
    pass


class Message(models.Model):
    author = models.ForeignKey('ChatUserInfo', related_name='author_messages', on_delete=models.CASCADE)
    replied_message = models.ForeignKey('Message', on_delete=models.SET_NULL)
    send_date = models.DateTimeField(auto_now_add=True)


class ImageMessage(Message):
    image = models.ImageField(upload_to='pictures/messages/')


class TextMessage(Message):
    text = models.CharField()


class Chat(models.Model, Profile):
    messages = models.ManyToManyField('Message', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


class MemberTypes:
    MEMBER = 'member'
    ADMIN = 'admin'
    OWNER = 'owner'


class ChatUserInfo(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    m_type = models.CharField(default=MemberTypes.MEMBER)
