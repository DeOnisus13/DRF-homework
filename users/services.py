import stripe
from currency_converter import CurrencyConverter
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def convert_rub_to_usd(amount):
    """Функция для перевода рублей в доллары"""
    try:
        c = CurrencyConverter()
        rate = c.convert(amount, "RUB", "USD")
        return round(rate)
    except:
        return amount * 90


def create_stripe_product(product_name):
    """Функция создания Stripe продукта"""
    return stripe.Product.create(name=product_name)


def create_stripe_price(amount, product):
    """Функция создания цены для Stripe"""
    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": product},
    )


def create_stripe_session(price):
    """Функция для создания сессии на оплату в Stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
