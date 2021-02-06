from channels.layers import get_channel_layer

from chat.managers import MyChatManager
from ood_project.consumers import ChatConsumer, EventHandler


def get_user_chat_consumer(user):
    chatConsumer = ChatConsumer()
    chatConsumer.user = user
    chatConsumer.channel_layer = get_channel_layer()
    return chatConsumer


class MyEventHandler(EventHandler):
    chat_manager = MyChatManager


class MyChatConsumer(ChatConsumer):
    event_handler = MyEventHandler



