from django.contrib import admin
from . import models

admin.site.register(models.UserProfile)
admin.site.register(models.Avatar)
admin.site.register(models.RequestModel)
admin.site.register(models.OpeningMessage)
admin.site.register(models.Interest)
admin.site.register(models.User)

