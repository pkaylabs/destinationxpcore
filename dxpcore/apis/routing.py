# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
# ]

from django.urls import re_path
from .consumers import ChatConsumer, NewChatConsumer

websocket_urlpatterns = [
    re_path(r"^chat/ws/test/$", ChatConsumer.as_asgi()), # Matches  ws://127.0.0.1:8000/chat/ws/test/
    re_path(r'ws/chat/(?P<room_name>\w+)/$', NewChatConsumer.as_asgi()),
]