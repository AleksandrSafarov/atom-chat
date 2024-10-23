from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .permissions import IsModerator, IsNotBlocked


class RegisterView(APIView):
    # Представление обрабатывает регистрацию пользователей
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Пользователь успешно зарегистрирован."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    # Представление, которое дает информация о пользователе по его id
    permission_classes = [IsAuthenticated, IsNotBlocked]

    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlockUserView(APIView):
    # Представление для блокировки пользователя по его id
    # Доступно только модераторам
    permission_classes = [IsAuthenticated, IsModerator, IsNotBlocked]

    def post(self, request, user_id):
        try:
            user_to_block = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        if user_to_block.is_blocked:
            return Response(
                {"message": f"Пользователь {user_to_block.username} уже заблокирован"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_to_block.is_blocked = True
        user_to_block.save()
        return Response(
            {"message": f"Пользователь {user_to_block.username} успешно заблокирован"},
            status=status.HTTP_200_OK,
        )


class PromoteToModeratorView(APIView):
    # Представление дает права модератора пользователю
    # Доступно только модераторам
    permission_classes = [IsAuthenticated, IsModerator, IsNotBlocked]

    def post(self, request, user_id):
        try:
            user_to_promote = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        if user_to_promote.is_moderator:
            return Response(
                {"message": f"Пользователь {user_to_promote.username} уже модератор"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_to_promote.is_moderator = True
        user_to_promote.save()
        return Response(
            {
                "message": f"Пользователь {user_to_promote.username} успешно получил права модератора"
            },
            status=status.HTTP_200_OK,
        )
