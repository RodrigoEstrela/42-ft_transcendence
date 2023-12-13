# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Chat
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_id = self.scope["user"].id
        # Find room object
        room = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)
        # Create chat object
        chat = Chat(
            content=message,
            user_id=user_id,
            room=room,
            timestamp=timezone.now(),
            username=self.scope["user"].username,
        )

        await database_sync_to_async(chat.save)()
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": message,
                "username": self.scope["user"].username,
                "timestamp": f"{chat.timestamp}"
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": f"{event['username']}",
            "timestamp": f"{event['timestamp']}"
        }))
