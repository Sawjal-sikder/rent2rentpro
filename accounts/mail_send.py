from django.core.mail import send_mail # type: ignore
from django.conf import settings # type: ignore
from celery import shared_task  # type: ignore

@shared_task
def Celery_send_mail(email, message, subject):
      send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])