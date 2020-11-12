from django.urls import path, include

from account import views
from .viewsets import *

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('userprofile/<slug:username>', views.get_user_profile_username),
    path('userprofile/update/<slug:username>', views.update_user_profile),
    path('opening_messages/', opening_message_list),
    path('opening_messages/<int:pk>', opening_message_detail),
    path('explore/suggested_opening_message/', explore),
]
