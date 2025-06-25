import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

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


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()
        print("WebSocket connection established.")
        # convert the message to JSON
        text_data = json.dumps({
            'message': 'WebSocket connection established.'
        })
        # Send a message to the client
        await self.send(text_data=text_data)
        

    async def disconnect(self, close_code):
        # Handle disconnection
        print("WebSocket connection closed.")

    async def receive(self, text_data):
        try:
            # Attempt to parse the incoming message as JSON
            data = json.loads(text_data)
            message = data.get('message', '')
        except json.JSONDecodeError:
            # If the message is not JSON, treat it as a plain string
            message = text_data

        if message == 'bye':
            text_data = json.dumps({
                'message': 'Server is shutting down.'
            })
            await self.send(text_data=text_data)
            await self.close()
        else:
            # Echo the message back to the client
            text_data = json.dumps({
                'message': f"Server received: {message}"
            })
            await self.send(text_data=text_data)
        print(f"Received message: {message}")