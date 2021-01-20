"""
ASGI config for trust_clinic project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# if these are not in this order it causes an application error
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trust_clinic.settings')
app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

application = ProtocolTypeRouter(
    {
        "http": app,
        "websocket": AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        ),
    }
)
