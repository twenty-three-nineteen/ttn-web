from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from ood_project.models import TextMessage, ChatUserInfo, Chat


class ChatManager:

    def __init__(self, chatId):
        self.chat = get_object_or_404(Chat, chatId)

    def get_last_10_messages(self, loaded_messages_number):
        return self.chat.messages.order_by('-send_date').all()[loaded_messages_number:loaded_messages_number + 10:-1]

    def create_text_message(self, author, text):
        message = TextMessage.objects.create(author=author, content=text)
        self.chat.messages.add(message)
        self.chat.save()

    def create_image_message(self, author, img):
        pass

    def join_the_chat(self, user):
        ChatUserInfo.objects.create(chat=self.chat, user=user)

    def left_the_chat(self, user):
        ChatUserInfo.objects.filter(chat=self.chat, user=user).delete()

    def promote(self, cui, member_type):
        pass

    def get_participants(self):
        chat_user_infos = ChatUserInfo.objects.filter(chat=self.chat)
        return [cui.user for cui in chat_user_infos.all()]

    def check_user_chat_access(self, user):
        if not (user in self.get_participants()):
            raise PermissionDenied('You do not have access to this chat.')


def messages_to_json(messages, chatId):
    result = []
    for message in messages:
        result.append(message_to_json(message, chatId))
    return result


def message_to_json(message, chatId):
    return {
        'id': message.id,
        'author': message.author.username,
        'content': message.content,
        'send_date': str(message.send_date),
        'chatId': chatId
    }
