from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import (convert_rub_to_usd, create_stripe_price,
                            create_stripe_product, create_stripe_session)


class UserViewSet(ModelViewSet):
    """ViewSet для модели пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class PaymentCreateAPIView(CreateAPIView):
    """Generic-класс для создания платежа"""

    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        product_name = payment.course.name
        stripe_product = create_stripe_product(product_name)
        amount_in_usd = convert_rub_to_usd(payment.course.price)
        stripe_price = create_stripe_price(amount_in_usd, stripe_product)
        session_id, payment_link = create_stripe_session(stripe_price)

        payment.payment_amount = amount_in_usd
        payment.session_id = session_id
        payment.link = payment_link

        payment.save()


class PaymentListAPIView(ListAPIView):
    """Generic-класс для вывода списка платежей"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("course", "lesson", "payment_method",)
    ordering_fields = ("payment_date",)
