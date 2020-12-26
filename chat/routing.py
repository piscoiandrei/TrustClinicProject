from django.urls import re_path
from .consumers import *

websocket_urlpatterns = [
    re_path(r'ws/chat/listener/$', Listener.as_asgi()),
    re_path(r'ws/chat/activator/$', Activator.as_asgi()),
    re_path(r'ws/chat/(?P<chat_id>\w+)/$', ChatHandler.as_asgi()),
]
