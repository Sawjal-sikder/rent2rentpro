from rest_framework import serializers #type: ignore
from accounts.models import PasswordResetCode #type: ignore
from django.contrib.auth import get_user_model #type: ignore
User = get_user_model()

class UserForgotPasswordVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    
    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "No active user found with this email."})
        
        try:
            verification_code = PasswordResetCode.objects.get(user=user, code=code, is_used=False)
        except PasswordResetCode.DoesNotExist:
            raise serializers.ValidationError({"message": "Invalid or used verification code."})
        
        verification_code.is_verified = True
        verification_code.save()
        
        self.user = user
        self.verification_code = verification_code
        return data