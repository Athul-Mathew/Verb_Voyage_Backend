

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Message
from Accounts.models import UserAccount
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # this is a nested dictionary and it will return the room_id which we are passing through the url
        current_user_id = self.scope['url_route']['kwargs']['id']
        # other_user_id = int(self.scope['query_string'])
        # print(other_user_id)

        self.room_id = current_user_id
        self.room_group_name = f'chat_{self.room_id}'

        # the channel_layer.group_add() takes two arguments
        # the name of the group to add the connection to --> self.room_group_name
        # and the name of the websocket connection ---> self.channel_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await super().disconnect(close_code)

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        message = data["message"]
        id = data["sender"]
        receiver_id = data['receiver_id']

        print("This is the receiver id: ", receiver_id)

        await self.save_message(
            sender=id, receiver=receiver_id, message=message, thread_name=self.room_group_name
        )

        print("This is the channel group name: ", self.room_group_name)

        # Send the message to the channel layer
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "senderID": id,
                "receiver_id": receiver_id,
            },
        )

    async def chat_message(self, event):
        print("Its entering here alright!!!")

        message = event["message"]
        id = event["senderID"]
        receiver = event["receiver_id"]

        await self.send(
            text_data=json.dumps(

                {
                    "message": message,
                    "senderID": id,
                    "receiver_id": receiver,
                }
            ),

        )

    @database_sync_to_async
    def save_message(self, sender, receiver, message, thread_name):
        receiver_instance = UserAccount.objects.get(id=int(receiver))
        user_instance = UserAccount.objects.get(id=sender)

        Message.objects.create(
            sender=user_instance, receiver=receiver_instance, message=message, thread_name=thread_name)

