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
        # remove the channel from the group
        async_to_sync(self.channel_layer.group_discard)(
            'listener',
            self.channel_name,
        )

    # receive message from websocket
    def receive(self, text_data=None, bytes_data=None):
        """
        Only the websocket from the client-side will send messages,
        so we don't need to check if the scpoe['user'] is client/operator
        """
        data = json.loads(text_data)
        connected_operators = User.objects.filter(is_connected=True)
        if not connected_operators:
            async_to_sync(self.channel_layer.group_send)(
                'listener',
                {  # type = the method that will be called
                    # when data is received from the group
                    'type': 'listener_data',
                    'available': 'false',
                    'source': data['id'],
                }
            )
        else:

            operator = connected_operators[
                random.randint(0, len(connected_operators) - 1)]
            client = get_object_or_404(User, email=self.scope['user'])
            async_to_sync(self.channel_layer.group_send)(
                'listener',
                {
                    'type': 'listener_data',
                    'available': 'true',
                    'operator': {
                        'id': operator.id,
                        'fullname': operator.full_name,
                        'email': operator.email,
                        'chat_id': client.id,
                    },
                    'client': {
                        'id': client.id,
                        'fullname': client.full_name,
                        'email': client.email,
                        'phone': client.phone,
                        'chat_id': client.id,
                    }
                }
            )

    # receive data from group
    def listener_data(self, event):
        available = event['available']
        if available == 'false':
            self.send(text_data=json.dumps({
                'available': 'false',
                'endpoint': event['source'],
            }))
        elif available == 'true':
            self.send(text_data=json.dumps({
                'available': 'true',
                'operator': {
                    'id': event['operator']['id'],
                    'fullname': event['operator']['fullname'],
                    'email': event['operator']['email'],
                    'chat_id': event['operator']['chat_id'],
                },
                'client': {
                    'id': event['client']['id'],
                    'fullname': event['client']['fullname'],
                    'email': event['client']['email'],
                    'phone': event['client']['phone'],
                    'chat_id': event['client']['chat_id'],
                }
            }))


class ChatHandler(WebsocketConsumer):
    def connect(self):
        # gets the chat_id from routing.py
        # self.scope['url_route']['kwargs']['chat_id']

        self.chat_group_name = self.scope['url_route']['kwargs']['chat_id']

        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name,
            self.channel_name,
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'source': data['source'],
                'endpoint': data['endpoint'],
                'message': data['message'],
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'source': event['source'],
            'endpoint': event['endpoint'],
            'message': event['message'],
        }))
