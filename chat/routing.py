from django.urls import re_path
from .consumers import *

websocket_urlpatterns = [
    re_path(r'ws/chat/activator/$', Activator.as_asgi()),
    re_path(r'ws/chat/$', ChatHandler.as_asgi()),
]
