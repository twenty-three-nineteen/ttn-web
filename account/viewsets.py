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

user_profile = UserProfileViewSet.as_view({
    'get': 'get_user_profile_username',
    'put': 'update_user_profile'
})
