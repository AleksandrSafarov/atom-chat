from rest_framework import serializers
from .models import Channel, Message
from users.models import CustomUser


class ChannelSerializer(serializers.ModelSerializer):
    # Сериализатор для создания нового канала
    # Определяет поля и валидацию для данных, вводимых при создании канала
    class Meta:
        model = Channel
        fields = ["id", "name", "password", "participants"]

    participants = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), many=True, required=False
    )

    def create(self, validated_data):
        participants = validated_data.pop("participants", [])
        channel = Channel.objects.create(**validated_data)

        request_user = self.context["request"].user
        channel.participants.add(request_user)

        if participants:
            channel.participants.add(*participants)

        return channel


class MessageSerializer(serializers.ModelSerializer):
    # Сериализатор для создания новго сообщения в канале
    # и преобразует данные модели Message в JSON формат и обратно
    class Meta:
        model = Message
        fields = ["id", "text", "created_at", "channel", "sender"]
        read_only_fields = ["created_at", "sender", "channel"]

    def create(self, validated_data):
        request_user = self.context["request"].user
        channel = self.context["channel"]
        message = Message.objects.create(
            sender=request_user, channel=channel, **validated_data
        )
        return message
