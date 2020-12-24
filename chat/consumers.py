import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class Listener(WebsocketConsumer):
    def connect(self):
        pass

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        pass


class Activator(WebsocketConsumer):
    def connect(self):
        pass

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        pass


class ChatHandler(WebsocketConsumer):
    def connect(self):
        # gets the user_id from routing.py
        # self.scope['url_route']['kwargs']['user_id']
        pass

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        pass
