from rest_framework import serializers #type: ignore
from accounts.models import PasswordResetCode #type: ignore
from django.contrib.auth import get_user_model #type: ignore
User = get_user_model()

class UserForgotSetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "No active user found with this email."})
        
        try:
            verification_code = PasswordResetCode.objects.filter(user=user, is_verified=True, is_used=False).first()
            if not verification_code:
                raise serializers.ValidationError({"message": "No verified password reset request found for this user."})
        except PasswordResetCode.DoesNotExist:
            raise serializers.ValidationError({"message": "No verified password reset request found for this user."})
        
        if password != confirm_password:
            raise serializers.ValidationError({"message": "Password and confirm password do not match."})
        
        # save password
        user.set_password(confirm_password)
        user.save()
        
        verification_code.is_used = True
        verification_code.save()
        
        self.user = user
        self.verification_code = verification_code
        self.confirm_password = confirm_password
        return data