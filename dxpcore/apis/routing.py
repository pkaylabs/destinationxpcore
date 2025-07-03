from django.urls import re_path

from apis.consumers import ChatRoomsConsumer, NewChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', NewChatConsumer.as_asgi()),
    re_path(r'ws/chatrooms/$', ChatRoomsConsumer.as_asgi()), # New route for chatrooms list
]