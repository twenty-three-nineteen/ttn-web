import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .managers import ChatManager, messages_to_json, message_to_json


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = self.scope['user']
        self.event_handler = EventHandler(self, self.user)

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.user.username,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.user.username,
            self.channel_name
        )

    def send_event(self, message, users):
        for user in users:
            async_to_sync(self.channel_layer.group_send)(
                user.username,
                {
                    'type': 'receive_event',
                    'message': message
                }
            )

    def receive_event(self, event):
        message = event['message']
        self.send_message(message)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        self.event_handler.handle(data)


class EventHandler(object):

    def __init__(self, chat_consumer, user):
        self.user = user
        self.chat_consumer = chat_consumer

    def fetch_messages(self, data):
        chat_mgr = ChatManager(data['chatId'])
        chat_mgr.check_user_chat_access(self.user)
        messages = chat_mgr.get_last_10_messages(data['loaded_messages_number'])
        event = {
            'command': 'messages',
            'messages': messages_to_json(messages, data['chatId'])
        }
        self.chat_consumer.send_message(event)

    def new_message(self, data):
        chat_mgr = ChatManager(data['chatId'])
        chat_mgr.check_user_chat_access(self.user)
        chat_mgr.create_text_message(self.user, data['message'])
        event = {
            'command': 'new_message',
            'message': message_to_json(data['message'], data['chatId'])
        }
        self.chat_consumer.send_event(event, chat_mgr.get_participants())

    def join(self, data):
        chat_mgr = ChatManager(data['chatId'])
        chat_mgr.join_the_chat(self.user)
        event = {
            'command': 'join_the_group',
            'message': {
                'username': self.user.username,
                'chatId': data['chatId']
            }
        }
        self.chat_consumer.send_event(event, chat_mgr.get_participants())

    def left(self, data):
        chat_mgr = ChatManager(data['chatId'])
        chat_mgr.join_the_chat(self.user)
        event = {
            'command': 'left_the_group',
            'message': {
                'username': self.user.username,
                'chatId': data['chatId']
            }
        }
        self.chat_consumer.send_event(event, chat_mgr.get_participants())

    def handle(self, data):
        self.event_types[data['command']](self, data)

    event_types = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'join': join,
        'left': left
    }
