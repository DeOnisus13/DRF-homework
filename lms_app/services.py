from django.conf import settings
from django.core.mail import send_mail


def send_update_course_email(recipients, course_name):
    """Функция отправки письма пользователям об изменении курса"""
    send_mail(
        subject=f"Изменения в курсе {course_name}",
        message=f"Содержание курса {course_name} изменилось. Посмотрите изменения",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipients,
        fail_silently=True
    )
