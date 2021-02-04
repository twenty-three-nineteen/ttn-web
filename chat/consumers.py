import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

from .models import Message
from .views import get_last_10_messages, get_current_chat, check_user_chat_access, get_avatar_id


def get_user_chat_consumer(user):
    chatConsumer = ChatConsumer()
    chatConsumer.user = user
    chatConsumer.channel_layer = get_channel_layer()
    return chatConsumer


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        check_user_chat_access(self.user, data['chatId'])
        if 'loaded_messages_number' in data:
            messages = get_last_10_messages(data['chatId'], data['loaded_messages_number'])
        else:
            messages = get_last_10_messages(data['chatId'], 0)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages, data['chatId'])
        }
        self.send_message(content)

    def new_message(self, data):
        self.create_new_message(data['message'], data['chatId'])

    def create_new_message(self, message, chatId):
        check_user_chat_access(self.user, chatId)
        author_user = self.user
        message = Message.objects.create(
            author=author_user,
            content=message)
        current_chat = get_current_chat(chatId)
        current_chat.messages.add(message)
        current_chat.save()
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message, chatId)
        }
        return self.send_chat_message(content, current_chat.participants.all())

    def messages_to_json(self, messages, chatId):
        result = []
        for message in messages:
            result.append(self.message_to_json(message, chatId))
        return result

    def message_to_json(self, message, chatId):
        return {
            'id': message.id,
            'author': message.author.username,
            'avatarId': get_avatar_id(message.author),
            'content': message.content,
            'send_date': str(message.send_date),
            'chatId': chatId
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.user = self.scope['user']
        self.room_group_name = self.user.username
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message, participants):
        for participant in participants:
            participant_group_name = participant.username
            async_to_sync(self.channel_layer.group_send)(
                participant_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
