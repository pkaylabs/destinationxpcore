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
            # Send chat history on connect
            await self.send_chat_history()
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
                    'username': self.user.email,
                }
            )
        elif message_type == 'stop_typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'stop_typing_notification',
                    'username': self.user.email,
                }
            )
        elif message:  # Normal chat message
            recipient = data.get('recipient')
            # Save the message to the database
            await self.save_message(self.room_name, self.user, message)
            from datetime import datetime
            timestamp = datetime.utcnow().isoformat()
            if recipient:
                # Individual chat
                recipient_group_name = f'user_{recipient}'
                await self.channel_layer.group_send(
                    recipient_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': self.user.email,
                        'email': self.user.email,
                        'timestamp': timestamp
                    }
                )
            else:
                # Group chat
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': self.user.name,
                        'email': self.user.email,
                        'timestamp': timestamp
                    }
                )

    @database_sync_to_async
    def save_message(self, room_name, sender, content):
        from .models import ChatRoom, Message
        try:
            room = ChatRoom.objects.get(name=room_name)
            Message.objects.create(room=room, sender=sender, content=content)
        except ChatRoom.DoesNotExist:
            pass

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'email': event.get('email', None),
            'message': event['message'],
            'timestamp': event.get('timestamp', None)
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

    @database_sync_to_async
    def get_chat_history(self):
        from .models import ChatRoom, Message
        try:
            room = ChatRoom.objects.get(name=self.room_name)
            messages = Message.objects.filter(room=room).order_by('timestamp')
            print(f"Retrieved {messages.count()} messages for room {self.room_name}")
            print(f"Messages: {[msg.content for msg in messages]}")
            return [
                {
                    'id': msg.id,
                    'sender': msg.sender.name,
                    'email': msg.sender.email,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat()
                }
                for msg in messages
            ]
        except ChatRoom.DoesNotExist:
            return []

    async def send_chat_history(self):
        history = await self.get_chat_history()
        await self.send(text_data=json.dumps({
            'type': 'chat_history',
            'messages': history
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
        """
        Return chatrooms where the user is a member,
        include `other_user` (if private) and the last message.
        """
        from .models import Message

        chatrooms = ChatRoom.objects.filter(members=self.user)

        result = []
        for room in chatrooms:
            data = {
                'id': room.id,
                'name': room.name,
                'is_group': room.is_group,
                'created_at': room.created_at.isoformat(),
            }

            # Add other user for private chats
            if not room.is_group:
                other_members = room.members.exclude(id=self.user.id)
                if other_members.exists():
                    data['other_user'] = other_members.first().name
                    # avatar
                    data['other_user_avatar'] = other_members.first().avatar.url if other_members.first().avatar else ''
                else:
                    data['other_user'] = None
                    data['other_user_avatar'] = ''

            # Fetch last message
            last_message = (
                Message.objects.filter(room=room)
                .order_by('-timestamp')
                .first()
            )

            if last_message:
                data['last_message'] = {
                    'text': last_message.content,
                    'created_at': last_message.timestamp.isoformat(),
                    'sender': last_message.sender.name,
                }
            else:
                data['last_message'] = None

            result.append(data)

        return result


    async def send_chatrooms_list(self):
        chatrooms = await self.get_chatrooms()
        await self.send(text_data=json.dumps({
            'type': 'chatrooms_list',
            'chatrooms': chatrooms
        }, default=str))