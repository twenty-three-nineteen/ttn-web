from django.urls import path

from .views import room

urlpatterns = [
    path('<int:chatId>/', room, name='room'),
]