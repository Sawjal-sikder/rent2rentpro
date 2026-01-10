from rest_framework import generics #type: ignore
from rest_framework import permissions #type: ignore
from rest_framework.response import Response #type: ignore
from ..serializers.user_forgot_password import UserForgotPasswordSerializer #type: ignore

class UserForgotPasswordView(generics.GenericAPIView):
    serializer_class = UserForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]  

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        varification_code = serializer.save()
        
        return Response({
            "message": "Password reset code sent successfully.",
            "details": f"A password reset code has been sent to {varification_code.user.email}.",
        })