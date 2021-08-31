from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = get_task_logger(__name__)


@shared_task
def send_email(subject, text_message, html_message, recipient_list):
    if settings.EMAIL_MODE == 'smtp':
        logger.info('Sending email to %s with smtp', recipient_list)
        send_mail(
            subject=subject,
            message=text_message,
            from_email=None,
            recipient_list=recipient_list,
            html_message=html_message,
        )
    elif settings.EMAIL_MODE == 'sendgrid':
        logger.info('Sending email to %s with sendgrid', recipient_list)
        message = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=recipient_list,
            subject=subject,
            html_content=html_message,
            plain_text_content=text_message,
        )
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        logger.debug('Received sendgrid response: %s', response)
    else:
        raise ValueError('Sending emails is disabled in current environment')
