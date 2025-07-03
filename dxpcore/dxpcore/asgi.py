"""
ASGI config for dxpcore project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dxpcore.settings')
import django
django.setup()

from django.core.asgi import get_asgi_application
from django.conf import settings
# for websocket
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apis.routing import websocket_urlpatterns



# Get the ASGI application for HTTP requests
application = get_asgi_application()

# Configure the ASGI application
application = ProtocolTypeRouter({
    "http": application,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})