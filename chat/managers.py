from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.exceptions import PermissionDenied

from chat.models import MyChat, MyMessage, MyChatUserInfo
from ood_project.managers import ChatManager


class MyChatManager(ChatManager):
    chat_model = MyChat
    text_message_model = MyMessage
    chat_user_info_model = MyChatUserInfo

    def left_the_chat(self, user):
        super().left_the_chat(user)
        if len(self.get_participants()) < 2:
            self.chat.status = MyChat.INACTIVE

    def check_user_chat_access(self, user):
        if not (user in self.get_participants()):
            raise PermissionDenied('You do not have access to this chat.')
        if self.chat.status == MyChat.INACTIVE:
            raise PermissionDenied('This chat is inactive.')


class NotificationManager:
    def send_join_notification(self, username, chatId, participants):
        self.send_notification('join_the_group', username, chatId, participants)

    def send_leave_notification(self, username, chatId, participants):
        self.send_notification('left_the_group', username, chatId, participants)

    def send_notification(self, command, username, chatId, participants):
        content = {
            'command': command,
            'message': {
                'username': username,
                'chatId': chatId
            }
        }
        channel_layer = get_channel_layer()
        for participant in participants:
            participant_group_name = participant.username
            async_to_sync(channel_layer.group_send)(
                participant_group_name,
                {
                    'type': 'chat_message',
                    'message': content
                }
            )
