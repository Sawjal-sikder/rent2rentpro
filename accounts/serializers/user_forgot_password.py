from rest_framework import serializers #type: ignore
from accounts.models import PasswordResetCode #type: ignore
from ..mail_send import Celery_send_mail #type: ignore
from django.contrib.auth import get_user_model #type: ignore
User = get_user_model()

class UserForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "No active user found with this email."})
        
        self.user = user
        return value
    
    def create(self, validated_data):
        # Logic to create a password reset code
        varification_code = PasswordResetCode.objects.create(user=self.user)
        # Send password reset email asynchronously
        Celery_send_mail.delay(
            email = self.user.email,
            subject = "Password Reset Request",
            message = (
                f"Hello {self.user.full_name},\n\n"
                f"We received a request to reset your password. Use the following code to reset it:\n"
                f"Your password reset code: {varification_code.code}\n\n"
                f"If you did not request a password reset, please ignore this email.\n\n"
                f"Best regards,\n"
                f"Support Team"
            )
        )
        return varification_code