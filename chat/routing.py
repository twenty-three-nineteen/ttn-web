from django.urls import path

from .consumers import MyChatConsumer

websocket_urlpatterns = [
    path('ws/chat/', MyChatConsumer.as_asgi()),
]