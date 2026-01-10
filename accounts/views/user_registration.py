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
        res_data = {
                "message": "User registered successfully. Please check your email to activate your account.",
                "user_details": f"A new activation code has been sent to {user.email}. Please check your email and activate your account.",
            }
        return Response(res_data, status=201)
                