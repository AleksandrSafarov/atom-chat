from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Кастомная модель пользователя
    # Добавляет 2 новых поля (is_blocked и is_moderator)
    is_blocked = models.BooleanField(default=False, verbose_name="Заблокирован")
    is_moderator = models.BooleanField(default=False, verbose_name="Модератор")

    def __str__(self):
        return self.username
