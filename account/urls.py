from django.urls import path, include
from account import views

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('restricted/', views.restricted),
    path('nextopeningmessage/', views.next_opening_message),
]
