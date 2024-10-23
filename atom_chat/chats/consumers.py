import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Channel, Message
from channels.db import database_sync_to_async


class ChannelConsumer(AsyncWebsocketConsumer):
    # Класс обрабатывает взаимодействие пользователей через WebSocket-соединение в чате

    async def connect(self):
        # Метод, вызываемый при установлении WebSocket-соединения
        headers = dict(
            (key.decode("utf-8"), value.decode("utf-8"))
            for key, value in self.scope["headers"]
        )
        token = headers.get("authorization")

        if token is None or not token.startswith("Bearer "):
            await self.close()
            return

        token = token.split()[1]

        try:
            UntypedToken(token)
        except InvalidToken:
            await self.close()
            return

        user = await self.get_user_from_token(token)

        if not user.is_authenticated:
            await self.close()
            return

        if user.is_blocked:
            await self.close()
            return

        self.channel_id = self.scope["url_route"]["kwargs"]["channel_id"]
        if not (await self.is_participant_or_moderator(user, self.channel_id)):
            await self.close()
            return

        self.channel_group_name = f"chat_{self.channel_id}"
        await self.channel_layer.group_add(self.channel_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Метод, вызываемый при разрыве WebSocket-соединения
        await self.channel_layer.group_discard(
            self.channel_group_name, self.channel_name
        )

    async def receive(self, text_data):
        # Метод для обработки сообщений, полученных через WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        token = (
            dict(
                (key.decode("utf-8"), value.decode("utf-8"))
                for key, value in self.scope["headers"]
            )
            .get("authorization")
            .split()[1]
        )
        user = await self.get_user_from_token(token)

        channel = await sync_to_async(Channel.objects.get)(id=self.channel_id)
        new_message = await sync_to_async(Message.objects.create)(
            sender=user, channel=channel, text=message
        )

        await self.channel_layer.group_send(
            self.channel_group_name,
            {
                "type": "chat_message",
                "message": new_message.text,
                "sender": user.username,
            },
        )

    async def chat_message(self, event):
        # Метод для отправки сообщений обратно пользователям через WebSocket
        message = event["message"]
        sender = event["sender"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "sender": sender,
                }
            )
        )

    @sync_to_async
    def is_participant_or_moderator(self, user, channel_id):
        # Метод проверяет, является ли пользователь участником канала или модератором
        try:
            channel = Channel.objects.get(id=channel_id)
            return channel.participants.filter(id=user.id).exists() or user.is_moderator
        except Channel.DoesNotExist:
            raise PermissionDenied("Канал не найден")

    @database_sync_to_async
    def get_user_from_token(self, token):
        # Метод для извлечения пользователя из JWT токена
        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_data.get("user_id")

        User = get_user_model()
        return User.objects.get(id=user_id)
