from accounts.mail_send import Celery_send_mail
from accounts.models import PasswordResetCode
import logging

logger = logging.getLogger(__name__)


def generate_otp(user):
    # Generate activation code
    activation_code = PasswordResetCode.objects.create(user=user)
                
    # Send welcome email asynchronously
    try:
        Celery_send_mail.delay(
            email = user.email,
            subject = "Activation of your new account!",
            message = (
                f"Hello {user.full_name},\n\n"
                f"Welcome! Your account has been successfully created.\n\n"
                f"Please activate your account and log into your account:\n"
                f"Your activation code: {activation_code.code}\n\n"
                f"We're excited to have you on board. If you have any questions or need assistance, feel free to reach out to our support team.\n\n"
                f"Best regards,\n"
                f"Support Team"
            )
        )
    except Exception as e:
        logger.error(f"Failed to send activation email: {e}")      