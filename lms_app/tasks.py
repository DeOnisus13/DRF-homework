from celery import shared_task

from lms_app.services import send_update_course_email


@shared_task
def update_course_mail(recipients, course_name):
    """Отложенная задача Celery для отправки писем об обновлении курса"""
    send_update_course_email(recipients, course_name)
