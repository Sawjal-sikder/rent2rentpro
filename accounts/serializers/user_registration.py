from rest_framework import serializers #type: ignore
from accounts.mail_send import Celery_send_mail  # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from ..models import PasswordResetCode
from ..utils_generate_otp import generate_otp

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)  # Override to remove unique validator

    class Meta:
        model = User
        fields = ['user_type','email', 'full_name', 'phone_number', 'password', 'profile_image']
        
    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if user:
            if not user.is_active:
                generate_otp(user)
                raise serializers.ValidationError({
                    "message": "This email is already registered but not activated. A new activation code has been sent to your email.",
                    "status": "resend_activation"
                })
            else:
                raise serializers.ValidationError({
                    "message": "A user with this email already exists. Please login. If you forgot your password, use the forgot password option.",
                    "status": "user_exists"
                })
        return value

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
        generate_otp(user) 
        
        return user