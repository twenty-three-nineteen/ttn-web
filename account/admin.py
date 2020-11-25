from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.Avatar)
admin.site.register(models.RequestModel)
admin.site.register(models.OpeningMessage)
