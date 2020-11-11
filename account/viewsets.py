from .views import *

opening_message_list = OpeningMessageViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

opening_message_detail = OpeningMessageViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

explore = ExploreViewSet.as_view({
    'get': 'get_suggested_opening_message'
})

