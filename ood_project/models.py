from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(models.Model):
    bio = models.CharField(max_length=255, default=None, null=True, blank=True)
    avatar = models.ImageField(upload_to='pictures/avatars/', null=True, blank=True)

    class Meta:
        abstract = True


class User(AbstractUser, Profile):

    class Meta:
        abstract = True


class Message(models.Model):
    # Foreign key to ChatUserInfo
    author = None
    # Foreign key to Message
    replied_message = None
    send_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ImageMessage(Message):
    image = models.ImageField(upload_to='pictures/messages/')

    class Meta:
        abstract = True


class TextMessage(Message):
    content = models.CharField(max_length=255)

    class Meta:
        abstract = True


class Chat(Profile):
    # Many to Many to Message
    messages = None
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class MemberTypes:
    MEMBER = 'member'
    ADMIN = 'admin'
    OWNER = 'owner'


class ChatUserInfo(models.Model):
    # Foreign key to User
    user = None
    # Foreign key to Chat
    chat = None
    m_type = models.CharField(max_length=30, default=MemberTypes.MEMBER)

    class Meta:
        abstract = True
