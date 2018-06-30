from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from chat.core.models.user import User


class ChatConsumer(WebsocketConsumer):

    def init_chat(self, data):
        username = data['username']
        user, created = User.objects.get_or_create(username=username)
        content = {
            'command': 'init_chat'
        }
        if not user:
            content['error'] = 'Unable to get or create User with username: ' + username
            self.send_message(content)
        content['success'] = 'Chatting in with success with username: ' + username
        self.send_message(content)


    def connect(self):
        self.room_name = 'room'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # leave group room
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
)
