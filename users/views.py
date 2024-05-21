from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    """ViewSet для модели пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentCreateAPIView(CreateAPIView):
    """Generic-класс для создания платежа"""

    serializer_class = PaymentSerializer


class PaymentListAPIView(ListAPIView):
    """Generic-класс для вывода списка платежей"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("course", "lesson", "payment_method",)
    ordering_fields = ("payment_date",)
