from rest_framework import serializers # type: ignore
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # type: ignore

class UserLoginSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        data = super().validate(attrs)
        return {
            "message": "Login successful",
            "user_details": {
                "email": self.user.email,
                "full_name": self.user.full_name,
                "phone_number": self.user.phone_number,
            },
            "refresh": data['refresh'],
            "access": data['access'],
        }