from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import Message, ItemRequest
from django.contrib.auth.models import User
from django.utils import timezone



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.item_id = self.scope['url_route']['kwargs']['item_id']
        self.other_user_id = self.scope['url_route']['kwargs']['other_user_id']
        self.room_name = f'chat_{self.item_id}_{self.other_user_id}'
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('content')
        sender_username = self.scope['user'].username

        # Save the message in the database by calling the standalone function
        await save_message(
            self.scope['user'].id, self.other_user_id, self.item_id, message
        )

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))
# Define save_message as a standalone function
@database_sync_to_async
def save_message(sender_id, receiver_id, item_id, content):
    sender = User.objects.get(id=sender_id)
    receiver = User.objects.get(id=receiver_id)
    item = ItemRequest.objects.get(id=item_id)
    return Message.objects.create(
        sender=sender,
        receiver=receiver,
        item=item,
        content=content,
        timestamp=timezone.now()
    )