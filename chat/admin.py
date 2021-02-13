from django.contrib import admin

from .models import MyMessage, MyChat, MyChatUserInfo

admin.site.register(MyMessage)
admin.site.register(MyChat)
admin.site.register(MyChatUserInfo)
