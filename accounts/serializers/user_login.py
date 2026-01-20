from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserLoginSerializer(TokenObtainPairSerializer):
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