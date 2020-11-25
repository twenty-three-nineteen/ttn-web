from django.urls import path, include

from account import views
from .viewsets import *

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('userprofile/<slug:username>', user_profile),
    path('opening_messages/', opening_message_list),
    path('opening_messages/<int:pk>', opening_message_detail),
    path('explore/suggested_opening_message/', explore),
    path('send_chat_request/', request_message),
    path('response_request/<slug:state>', response_request_message),
    path('myRequests/', user_requests),
]
