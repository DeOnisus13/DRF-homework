from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = ("id", "email", "phone", "password", "is_active", "is_staff", "is_superuser",)
