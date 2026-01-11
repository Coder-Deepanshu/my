import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Current login user aur target user ki ID se room name banayein
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        self.room_name = f'{min(my_id, int(other_user_id))}_{max(my_id, int(other_user_id))}'
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        receiver_id = data['receiver_id']

        # Database mein save karein
        await self.save_message(message, receiver_id)

        # Dusre user ko message bhejein
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope['user'].username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    @database_sync_to_async
    def save_message(self, message, receiver_id):
        receiver = User.objects.get(id=receiver_id)
        ChatMessage.objects.create(
            sender=self.scope['user'],
            receiver=receiver,
            message=message,
            thread_name=self.room_name
        )