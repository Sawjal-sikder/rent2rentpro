from rest_framework import generics #type: ignore
from rest_framework import permissions #type: ignore
from rest_framework.response import Response #type: ignore
from ..serializers.user_forgot_password_verification import UserForgotPasswordVerificationSerializer #type: ignore

class UserForgotPasswordVerificationView(generics.GenericAPIView):
    serializer_class = UserForgotPasswordVerificationSerializer
    permission_classes = [permissions.AllowAny]  

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response({
            "message": "Verification code is valid.",
            "details": f"The verification code for {serializer.user.email} is valid.",
        })