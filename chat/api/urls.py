from django.urls import path

from chat.api.viewsets import chat_list, chat_detail

app_name = 'chat'

urlpatterns = [
    path('', chat_list),
    path('<int:pk>/', chat_detail),
]
