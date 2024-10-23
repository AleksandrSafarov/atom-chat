from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Channel(models.Model):
    # Модель приватного канала
    name = models.CharField(max_length=255, verbose_name="Название канала")
    password = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="Пароль"
    )
    participants = models.ManyToManyField(
        User, related_name="channels", verbose_name="Участники"
    )

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"

    def __str__(self):
        return self.name


class Message(models.Model):
    # Модель сообщения
    text = models.TextField(verbose_name="Текст сообщения")
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Отправитель"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name="Канал")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]}..."
