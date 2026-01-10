from rest_framework import serializers #type: ignore
from accounts.models import PasswordResetCode #type: ignore
from django.contrib.auth import get_user_model #type: ignore
User = get_user_model()

class UserRegistrationActiveSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    
    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'], is_active=False)
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "No inactive user found with this email."})
        
        try:
            activation_code = PasswordResetCode.objects.get(
                user=user,
                code=data['code'],
                is_used=False
            )
        except PasswordResetCode.DoesNotExist:
            raise serializers.ValidationError({"message": "Invalid or already used activation code."})
        
        if activation_code.is_expired():
            raise serializers.ValidationError({"message": "The activation code has expired."})
        
        self.user = user
        self.activation_code = activation_code
        return data
    
    def save(self, **kwargs):
        self.user.is_active = True
        self.user.save()
        self.activation_code.is_used = True
        self.activation_code.save()
        return self.user