from .views import *

chat_list = MCUIViewSet.as_view({
    'get': 'list',
})

chat_detail = MCUIViewSet.as_view({
    'get': 'retrieve',
    'delete': 'left'
})
