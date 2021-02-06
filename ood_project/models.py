from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings


class Profile(models.Model):
    bio = models.CharField(max_length=255, default=None, null=True, blank=True)
    avatar = models.ImageField(upload_to='pictures/avatars/', null=True, blank=True)

    class Meta:
        abstract = True


class User(AbstractUser, Profile):

    class Meta:
        abstract = True


class Message(models.Model):
    author = models.ForeignKey(settings.OOD_FINAL_PROJECT['chat_user_info_model']
                               , related_name='author_messages',
                               on_delete=models.CASCADE)
    replied_message = models.ForeignKey(settings.OOD_FINAL_PROJECT['message_model'],
                                        on_delete=models.SET_NULL, null=True)
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

    message_model = None

    messages = models.ManyToManyField(settings.OOD_FINAL_PROJECT['message_model'], blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class MemberTypes:
    MEMBER = 'member'
    ADMIN = 'admin'
    OWNER = 'owner'


class ChatUserInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat = models.ForeignKey(settings.OOD_FINAL_PROJECT['chat_model'], on_delete=models.CASCADE)
    m_type = models.CharField(max_length=30, default=MemberTypes.MEMBER)

    class Meta:
        abstract = True
