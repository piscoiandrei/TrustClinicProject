import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class Listener(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        print(f'Listener----- {data}')


class Activator(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        print(f'Activatorr----- {data}')


class ChatHandler(WebsocketConsumer):
    def connect(self):
        # gets the user_id from routing.py
        # self.scope['url_route']['kwargs']['user_id']
        pass

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        pass
