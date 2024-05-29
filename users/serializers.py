from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    """Сериализатор для модели платежей"""

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """Сериализатор для модели пользователя"""

    payment_history = PaymentSerializer(source="user", many=True, read_only=True)

    class Meta:
        model = User
        exclude = ("password", "last_login", "date_joined", )
