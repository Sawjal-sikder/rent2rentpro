from rest_framework import serializers #type: ignore
from accounts.mail_send import Celery_send_mail  # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from ..models import PasswordResetCode

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone_number', 'password', 'profile_image']

    def create(self, validated_data):
        # Check if we're resending activation for existing user
        if self.context.get('resend_activation'):
            return self.context.get('existing_user')
        
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.is_active = False
        user.is_staff = False
        user.set_password(password)
        user.save()
        
        # Generate activation code
        activation_code = PasswordResetCode.objects.create(user=user)
                
        # Send welcome email asynchronously
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
        
        return user