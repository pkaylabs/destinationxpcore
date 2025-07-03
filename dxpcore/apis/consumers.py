import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom

logger = logging.getLogger(__name__)

class NewChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(f"Attempting to connect: {self.scope}")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = await self.get_user_from_token(self.scope['query_string'])

        if self.user:
            self.scope['user'] = self.user
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    @database_sync_to_async
    def get_user_from_token(self, query_string):
        from urllib.parse import parse_qs
        from knox.auth import TokenAuthentication

        parsed = parse_qs(query_string.decode())
        token = parsed.get("token", [None])[0]

        if not token:
            return None

        try:
            user_auth_tuple = TokenAuthentication().authenticate_credentials(token.encode())
            return user_auth_tuple[0]  # the user object
        except Exception as e:
            logger.warning(f"Token auth failed: {e}")
            return None

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        message_type = data.get('type')  # Optional

        if message_type == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_notification',
                    'username': self.user.username,
                }
            )
        elif message_type == 'stop_typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'stop_typing_notification',
                    'username': self.user.username,
                }
            )
        elif message:  # Normal chat message
            recipient = data.get('recipient')
            if recipient:
                # Individual chat
                recipient_group_name = f'user_{recipient}'
                await self.channel_layer.group_send(
                    recipient_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': self.user.username
                    }
                )
            else:
                # Group chat
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': self.user.username
                    }
                )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'message': event['message']
        }))

    async def typing_notification(self, event):
        await self.send(text_data=json.dumps({
            'typing': True,
            'username': event['username']
        }))

    async def stop_typing_notification(self, event):
        await self.send(text_data=json.dumps({
            'typing': False,
            'username': event['username']
        }))


class ChatRoomsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'chatrooms_updates'
        self.user = await self.get_user_from_token(self.scope['query_string'])
        if self.user:
            self.scope['user'] = self.user
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            await self.send_chatrooms_list()
        else:
            await self.close()

    @database_sync_to_async
    def get_user_from_token(self, query_string):
        from urllib.parse import parse_qs
        from knox.auth import TokenAuthentication
        parsed = parse_qs(query_string.decode())
        token = parsed.get("token", [None])[0]
        if not token:
            return None
        try:
            user_auth_tuple = TokenAuthentication().authenticate_credentials(token.encode())
            return user_auth_tuple[0]  # the user object
        except Exception as e:
            logger.warning(f"Token auth failed: {e}")
            return None

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Optionally handle client messages
        pass

    async def chatrooms_update(self, event):
        await self.send_chatrooms_list()

    @database_sync_to_async
    def get_chatrooms(self):
        # Only return chatrooms where the user is a member
        return list(ChatRoom.objects.filter(members=self.user).values('id', 'name', 'is_group', 'created_at'))

    async def send_chatrooms_list(self):
        chatrooms = await self.get_chatrooms()
        await self.send(text_data=json.dumps({
            'type': 'chatrooms_list',
            'chatrooms': chatrooms
        }, default=str))