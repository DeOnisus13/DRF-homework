from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentCreateAPIView, PaymentListAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
] + router.urls
