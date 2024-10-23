from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsModerator(permissions.BasePermission):
    # Разрешение для проверки, является ли пользователь моедартором
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.is_moderator
        )


class IsNotBlocked(permissions.BasePermission):
    # Разрешение для проверки, не является ли пользователь заблокированым
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.is_blocked:
                raise PermissionDenied("Пользователь заблокирован")
            return True
        return False
