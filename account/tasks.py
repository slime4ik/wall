from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

import logging
logger = logging.getLogger('account')

@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def send_code_to_email(email: str, code: str) -> None:
    try:
        subject = "Login attempt"
        message = (
            f"Your login code: {code}\n\n"
            "If you didn't try to login we reccomend you to change password as soon as possible"
        )
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(
            subject,
            message,
            from_email,
            [email],
            fail_silently=False,
        )
        logger.info(f"Verification code {code} sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send code to {email}: {e}")
        raise

@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def send_code_to_email_verify(email: str, code: str) -> None:
    try:
        subject = "Verify attempt"
        message = (
            f"Your verify code: {code}\n\n"
            "If you didn't try to verify your account on site: wehelpy.ru you can safety ignore this message."
        )
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(
            subject,
            message,
            from_email,
            [email],
            fail_silently=False,
        )
        logger.info(f"Verification code {code} sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send code to {email}: {e}")
        raise
