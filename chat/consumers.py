import json
import random
import logging
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)
User = get_user_model()
logstr = 'LOG  :::  '


@database_sync_to_async
def set_connection(email, bool_value):
    operator = get_object_or_404(User, email=email)

    if not operator.is_operator:
        raise ImproperlyConfigured(
            "The Operator should always have is_operator=True")

    operator.is_connected = bool_value
    logger.info(logstr + 'Operator state: ' + repr(operator))
    operator.save()


@database_sync_to_async
def get_connected_operators():
    """
     converting to list so we force the databse to execute the
     query immediately, if it's not converted, due to the fact that
     queries are lazy it will execute as an sync function somewhere
     later in the code, this is bad since we have async code
    """
    return list(User.objects.filter(is_connected=True))


class Activator(AsyncWebsocketConsumer):
    """
    The WsConsumer receives the user from auth middleware when it connects,
    then it's marked as connected
    """

    async def connect(self):
        """
        self.scope['user'] returns a unique identifier, in this case the email
        """
        logger.info(
            logstr + 'Activator is connecting: ' + self.scope['user'].email)
        await set_connection(self.scope['user'].email, True)
        await self.accept()

    async def disconnect(self, code):
        logger.info(logstr + 'Activator is disconnecting: ' + self.scope[
            'user'].email)
        await set_connection(self.scope['user'].email, False)


class ChatHandler(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'chat',  # group name
            self.channel_name
        )
        await self.accept()
        logger.info(logstr + 'The ChatHandler connected.')

    async def disconnect(self, close_code):
        user_email = self.scope['user'].email

        await self.channel_layer.group_send(
            'chat',
            {
                'type': 'chat_close',
                'endpoint_email': user_email,
            }
        )

        await self.channel_layer.group_discard(
            'chat',
            self.channel_name
        )
        logger.info(
            logstr + 'The ChatHandler for ' + user_email + ' disconnected.')

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        logger.info(
            logstr + 'The ChatHandler received data from ' + self.scope[
                'user'].email + ' WebSocket')
        logger.info(logstr + 'Data received: \n' + json.dumps(data, indent=2))

        # only the client sends 'init' type requests
        if data['action'] == 'init':
            connected_operators = await get_connected_operators()
            if connected_operators:
                operator = connected_operators[
                    random.randint(0, len(connected_operators) - 1)]

                await self.channel_layer.group_send(
                    'chat',
                    {
                        'type': 'chat_init',
                        'source': data['source'],
                        'endpoint': {
                            'email': operator.email,
                            'full_name': operator.full_name,
                        },
                    }
                )
            else:
                await self.channel_layer.group_send(
                    'chat',
                    {
                        'type': 'chat_unavailable',
                        'source': data['source'],
                    }
                )
        elif data['action'] == 'message':
            await self.channel_layer.group_send(
                'chat',
                {
                    'type': 'chat_message',
                    'source': data['source'],
                    'endpoint': data['endpoint'],
                    'message': data['message'],
                }
            )
        elif data['action'] == 'close':
            await self.channel_layer.group_send(
                'chat',
                {
                    'type': 'chat_close',
                    'endpoint_email': data['endpoint_email'],
                }
            )

    async def chat_init(self, event):
        data_to_send = json.dumps({
            'action': 'init',
            'source': event['source'],
            'endpoint': event['endpoint']

        }, indent=2)

        logger.info(logstr + 'Data sent: \n' + data_to_send)

        await self.send(text_data=data_to_send)

    async def chat_unavailable(self, event):
        data_to_send = json.dumps({
            'action': 'unavailable',
            'source': event['source'],

        }, indent=2)

        logger.info(logstr + 'Data sent: \n' + data_to_send)

        await self.send(text_data=data_to_send)

    async def chat_message(self, event):
        data_to_send = json.dumps({
            'action': 'message',
            'source': event['source'],
            'endpoint': event['endpoint'],
            'message': event['message'],
        }, indent=2)

        logger.info(logstr + 'Data sent: \n' + data_to_send)

        await self.send(text_data=data_to_send)

    async def chat_close(self, event):
        data_to_send = json.dumps({
            'action': 'close',
            'endpoint_email': event['endpoint_email']
        }, indent=2)

        logger.info(logstr + 'Data sent: \n' + data_to_send)

        await self.send(text_data=data_to_send)
