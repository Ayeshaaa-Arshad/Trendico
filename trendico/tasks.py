from email.mime.text import MIMEText
from django.conf import settings
from django.contrib.auth.models import User
from trendico.models import Order
from celery import shared_task
import smtplib

@shared_task
def send_order_notification_email(order_id):
        admin_emails = User.objects.filter(is_staff=True, is_superuser=True).values_list('email', flat=True)

        subject = 'New Order Placed'
        message = f'An order with ID {order_id} has been placed.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = admin_emails

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = ', '.join(recipient_list)

        try:
            smtp_server = smtplib.SMTP(
                settings.EMAIL_HOST, settings.EMAIL_PORT)
            smtp_server.starttls()

            smtp_server.login(settings.EMAIL_HOST_USER,
                              settings.EMAIL_HOST_PASSWORD)

            smtp_server.sendmail(from_email, recipient_list, msg.as_string())

            smtp_server.quit()

            print('Email sent successfully')
        except smtplib.SMTPException as e:
            print(f'Error Sending in email : {e}')

