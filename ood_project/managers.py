from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from ood_project.models import MemberTypes


class ChatManager:

    chat_model = None
    text_message_model = None
    chat_user_info_model = None

    def __init__(self, chatId):
        self.chat = get_object_or_404(self.chat_model, id=chatId)

    def get_last_10_messages(self, loaded_messages_number):
        return self.chat.messages.order_by('-send_date').all()[loaded_messages_number:loaded_messages_number + 10:-1]

    def create_text_message(self, author, text):
        author_cui = self.chat_user_info_model.objects.all().filter(chat=self.chat).get(user=author)
        message = self.text_message_model.objects.create(author=author_cui, content=text)
        self.chat.messages.add(message)
        self.chat.save()
        return message

    def create_image_message(self, author, img):
        pass

    def join_the_chat(self, user):
        self.chat_user_info_model.objects.create(chat=self.chat, user=user)

    def left_the_chat(self, user):
        self.chat_user_info_model.objects.filter(chat=self.chat, user=user).delete()

    def promote_to_admin(self, user, user_to_promote_id):
        cui = self.chat_user_info_model.objects.all().filter(chat=self.chat).get(user=user)
        cui_to_promote = self.chat_user_info_model.objects.all().filter(chat=self.chat).get(user__id=user_to_promote_id)
        if (cui.m_type == MemberTypes.ADMIN or cui.m_type == MemberTypes.OWNER)\
                and cui_to_promote.m_type == MemberTypes.MEMBER:
            cui_to_promote.m_type = MemberTypes.ADMIN
            cui_to_promote.save()
            return cui_to_promote.user
        else:
            raise PermissionDenied()

    def get_participants(self):
        chat_user_infos = self.chat_user_info_model.objects.filter(chat=self.chat)
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
        'author': message.author.user.username,
        'content': message.content,
        'send_date': str(message.send_date),
        'chatId': chatId
    }
