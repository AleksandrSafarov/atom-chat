from django.urls import re_path
from .consumers import ChannelConsumer

websocket_urlpatterns = [
    # Маршрут для WebSocket соединения
    # Запросы, соответствующие этому шаблону, будут обрабатываться асинхронным WebSocket-потребителем ChannelConsumer
    re_path(
        r"ws/channel/(?P<channel_id>\d+)/$",
        ChannelConsumer.as_asgi(),
    ),
]
