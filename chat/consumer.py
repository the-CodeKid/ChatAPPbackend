import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer (AsyncWebsocketConsumer):
    async def connect(self):
        from .models import Messages
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        history = await sync_to_async(list)(
            Messages.objects.filter(room=self.room_name).order_by('-timestamp')[:20]
        )

        for msg in reversed(history):
            await self.send(text_data=json.dumps({
                "text": msg.text,
                "username": msg.username,
                "file_url": msg.file_url,
                "file_name": msg.file_name,
            }))
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        from .models import Messages
        data = json.loads(text_data)
        message = data["text"]
        username = data.get("username", "Anonymous")
        file_url = data.get('file_url', '')
        file_name = data.get('file_name','')

        await sync_to_async(Messages.objects.create)(
            room = self.room_name,
            username = username,
            text = message,
            file_url = file_url,
            file_name = file_name,
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': message,
                'username': username,
                'file_name': file_name,
                'file_url': file_url,
            }
        )

    async def chat_message(self, event):
        message = event['text']
        await self.send(text_data = json.dumps({
            'text': message,
            'username': event.get("username", "Anonymous"),
            'file_name': event.get('file_name', ''),
            'file_url': event.get('file_url', '')
        }))