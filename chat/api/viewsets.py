from .views import *

chat_list = ChatViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

chat_detail = ChatViewSet.as_view({
    'get': 'retrieve',
    'delete': 'left'
})
