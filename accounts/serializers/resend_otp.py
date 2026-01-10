from rest_framework import serializers #type: ignore
from accounts.models import PasswordResetCode #type: ignore
from ..mail_send import Celery_send_mail #type: ignore
from django.contrib.auth import get_user_model #type: ignore
User = get_user_model()

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value, is_active=False)
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "No inactive user found with this email. Please register first."})
        
        if user.is_active:
            raise serializers.ValidationError({"message": "This user is already active. Please log in."})
        
        self.user = user
        return value
    
    def save(self, **kwargs):
        # Logic to resend OTP code
        otp_code = PasswordResetCode.objects.create(user=self.user)
        # Send OTP email asynchronously
        Celery_send_mail.delay(
            email = self.user.email,
            subject = "Activation of your new account!",
            message = (
                f"Hello {self.user.full_name},\n\n"
                f"Welcome! Your resend otp action has been successfully.\n\n"
                f"Please activate your account or reset your password and log into your account:\n"
                f"Your activation code: {otp_code.code}\n\n"
                f"We're excited to have you on board. If you have any questions or need assistance, feel free to reach out to our support team.\n\n"
                f"Best regards,\n"
                f"Support Team"
            )
        )  
        return self.user