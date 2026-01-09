from rest_framework import generics # type: ignore
from rest_framework import permissions as permission # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from rest_framework.response import Response # type: ignore

from ..serializers.user_registration import UserRegistrationSerializer # type: ignore

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permission.AllowAny]  
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Check if we resent activation code to existing user
        if serializer.context.get('resend_activation'):
            res_data = {
                "message": "Activation code resent successfully",
                "user_details": f"A new activation code has been sent to {user.email}. Please check your email and activate your account.",
            }
        else:
            res_data = {
                "message": "User registered successfully",
                "user_details": f"Please activate your account using the activation code sent to {user.email}",
            }
        
        return Response(res_data, status=201)
                