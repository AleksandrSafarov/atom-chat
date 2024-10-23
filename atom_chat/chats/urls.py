from django.urls import path
from .views import (
    ChannelCreateView,
    ChannelPasswordCheckView,
    MessageCreateView,
    MessageListView,
)

urlpatterns = [
    # URL для создания нового канала
    # Обрабатывается представлением ChannelCreateView
    path(
        "create/",
        ChannelCreateView.as_view(),
        name="channel_create",
    ),
    # URL для ввода и проверки пароля для канала
    # Обрабатывается представлением ChannelPasswordCheckView
    path(
        "<int:channel_id>/check-password/",
        ChannelPasswordCheckView.as_view(),
        name="check_password",
    ),
    # URL для создания сообщения в канале
    # Обрабатывается представлением MessageCreateView
    path(
        "<int:channel_id>/create-message/",
        MessageCreateView.as_view(),
        name="create_message",
    ),
    # URL для вывода всех сообщений канала по его id
    # Обрабатывается представлением MessageListView
    path(
        "<int:channel_id>/messages/",
        MessageListView.as_view(),
        name="all_message",
    ),
]
