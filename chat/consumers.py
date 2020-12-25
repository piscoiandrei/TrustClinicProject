import json
import random
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404

# database_sync_to_async is not needed yet, because
# the code is written synchronously

User = get_user_model()


def set_connection(operator_id, bool_value):
    operator = get_object_or_404(User, pk=int(operator_id))

    if not operator.is_operator:
        raise ImproperlyConfigured(
            "The Operator should always have is_operator=True")

    operator.is_connected = bool_value
    operator.save()


def get_user_by_email(email) -> int:
    user = get_object_or_404(User, email=email)
    return user.id


class Activator(WebsocketConsumer):
    """
    The WsConsumer receives the user from auth middleware when it connects,
    then it's marked as connected
    """

    def connect(self):
        """
        self.scope['user'] returns a unique identifier, in this case the email
        """
        set_connection(get_user_by_email(self.scope['user']), True)
        self.accept()

    def disconnect(self, code):
        set_connection(get_user_by_email(self.scope['user']), False)


class Listener(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'listener',  # group name
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # remove the ws from the group
        async_to_sync(self.channel_layer.group_discard)(
            'listener',
            self.channel_name,
        )

    # receive message from websocket
    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        connected_operators = User.objects.filter(is_connected=True)
        if not connected_operators:
            async_to_sync(self.channel_layer.group_send)(
                'listener',
                {
                    'type': 'listener_data',
                    'available': 'false',
                    'source': data['id'],
                }
            )
        else:
            pass

    # receive data from group
    def listener_data(self, event):
        available = event['available']
        if available == 'false':
            self.send(text_data=json.dumps({
                'available': 'false',
                'endpoint': event['source'],
            }))
        else:
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
