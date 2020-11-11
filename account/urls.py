from django.urls import path, include
from account import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('restricted/', views.restricted),
    path('nextopeningmessage/', views.next_opening_message),
    path('userprofile/<username>', views.get_user_profile_username),
    path('userprofile/update/<username>', views.update_user_profile),
]
