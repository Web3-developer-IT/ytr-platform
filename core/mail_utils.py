import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_platform_mail(subject, message, recipient_list, *, from_email=None):
    """
    Send transactional mail. Returns (ok: bool, error: str|None).
    Logs failures; does not swallow SMTP errors silently.
    """
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    if not recipient_list:
        return False, "No recipient configured."
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return True, None
    except Exception:
        logger.exception("Platform email send failed: %s", subject)
        return False, "Email could not be sent from this server. Please try again later or phone support."


def feedback_recipients():
    """Primary inbox for contact + feedback forms."""
    addr = getattr(settings, "CLIENT_FEEDBACK_EMAIL", None) or settings.BUSINESS_CONTACT_EMAIL
    return [addr]
