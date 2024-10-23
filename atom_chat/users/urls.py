from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, UserView, BlockUserView, PromoteToModeratorView

urlpatterns = [
    # URL для регистрации нового пользователя
    # Обрабатывается представлением RegisterView
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    # URL для получения JWT токена (вход в систему)
    # Обрабатывается стандартным представлением TokenObtainPairView для получения пары токенов (доступа и обновления)
    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    # URL для обновления JWT токена доступа
    # Обрабатывается стандартным представлением TokenRefreshView
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    # URL для получения информации о пользователе по его id
    # Обрабатывается представлением UserView
    path(
        "user/<int:user_id>/",
        UserView.as_view(),
        name="user",
    ),
    # URL для блокировки пользователя по его id
    # Обрабатывается представлением BlockUserView
    path(
        "block-user/<int:user_id>/",
        BlockUserView.as_view(),
        name="block_user",
    ),
    # URL для предоставления прав модератора пользователю по его id
    # Обрабатывается представлением PromoteToModeratorView
    path(
        "promote-to-moderator/<int:user_id>/",
        PromoteToModeratorView.as_view(),
        name="promote_to_moderator",
    ),
]
