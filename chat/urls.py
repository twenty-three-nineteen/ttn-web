from django.urls import path

from .views import room

urlpatterns = [
    path('', room, name='room'),
]