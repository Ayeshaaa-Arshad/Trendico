from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from celery import shared_task
import smtplib

@shared_task
def send_order_notification_email(order_id):
    admin_emails = list(User.objects.filter(is_staff=True, is_superuser=True).values_list('email', flat=True))
    subject = 'New Order Placed'
    message = f'An order with ID {order_id} has been placed.'

    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            to=admin_emails,
            from_email=settings.DEFAULT_FROM_EMAIL,
        )
        email.send()
        print('Email sent successfully')
    except smtplib.SMTPException as e:
        print(f'Error Sending in email : {e}')
