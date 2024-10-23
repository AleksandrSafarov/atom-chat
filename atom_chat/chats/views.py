from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsNotBlocked
from .serializers import ChannelSerializer, MessageSerializer
from .models import Channel, Message


class ChannelCreateView(APIView):
    # Представление создает новый канал
    permission_classes = [IsAuthenticated, IsNotBlocked]

    def post(self, request):
        serializer = ChannelSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChannelPasswordCheckView(APIView):
    # Представление для поверки введенного пароля для канала
    permission_classes = [IsAuthenticated, IsNotBlocked]

    def post(self, request, channel_id):
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            return Response(
                {"error": "Канал не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        if channel.password == request.data.get("password"):
            user = request.user
            if channel.participants.filter(id=user.id).exists():
                return Response(
                    {
                        "message": f"Пользователь {user.username} уже является участником канала {channel.name}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            channel.participants.add(user)
            return Response(
                {
                    "message": f"Введён корректный пароль. Пользователь {user.username} стал участником канала {channel.name}"
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Введён некорректный пароль"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class MessageCreateView(APIView):
    # Представление для создания нового сообщения в канале
    # Доступно пользователям-участникам канала и модераторам
    permission_classes = [IsAuthenticated, IsNotBlocked]

    def post(self, request, channel_id):
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            return Response(
                {"error": "Канал не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        user = request.user
        if channel.participants.filter(id=user.id).exists() or user.is_moderator:
            serializer = MessageSerializer(
                data=request.data, context={"request": request, "channel": channel}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "message": f"Пользователь {user.username} не является участником канала {channel.name}"
            },
            status=status.HTTP_403_FORBIDDEN,
        )


class MessageListView(ListAPIView):
    # Представление для вывода всех сообщений канала по его id
    # Доступно пользователям-участникам канала и модераторам
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsNotBlocked]

    def get_queryset(self):
        channel_id = self.kwargs["channel_id"]
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            raise Http404("Канал не найден")
        user = self.request.user
        if channel.participants.filter(id=user.id).exists() or user.is_moderator:
            return Message.objects.filter(channel_id=channel_id).order_by("created_at")
        raise PermissionDenied(
            f"Пользователь {user.username} не является участником канала {channel.name}"
        )
