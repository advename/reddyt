import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class NotificationConsumer(WebsocketConsumer):
    # WebsocketConsumer is a generic Django Channel class handling connect, disconnect and receive activities

    def connect(self):
        self.accept()  # this is required to accept a connection call
        user = self.scope["user"]
        user_room = f"user-{user.id}"
        # <- each user belongs to their unique user group
        async_to_sync(self.channel_layer.group_add)(
            user_room, self.channel_name)

    def disconnect(self, close_code):
        user = self.scope["user"]
        user_room = f"user-{user.id}"
        async_to_sync(self.channel_layer.group_discard)(
            user_room, self.channel_name)

    def receive(self, text_data):  # <- text_data is default. You cant change this value
        # This method is usually used to receive websockets messages from the client
        # This method is not needed for our case, since we dont want to listen to incoming websocket messages
        pass

    def send_message(self, event):
        self.send(text_data=json.dumps({
            "notification": event['notification']
        }))
