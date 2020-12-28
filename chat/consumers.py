import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Message
from .views import get_last_10_messages, get_current_chat, check_user_chat_access


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        check_user_chat_access(self.user, data['chatId'])
        messages = get_last_10_messages(data['chatId'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages, data['chatId'])
        }
        self.send_message(content)

    def new_message(self, data):
        check_user_chat_access(self.user, data['chatId'])
        author_user = self.user
        message = Message.objects.create(
            author=author_user,
            content=data['message'])
        current_chat = get_current_chat(data['chatId'])
        current_chat.messages.add(message)
        current_chat.save()
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message, data['chatId'])
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
