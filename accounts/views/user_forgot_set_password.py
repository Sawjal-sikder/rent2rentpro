from rest_framework import generics #type: ignore
from rest_framework import permissions #type: ignore
from rest_framework.response import Response #type: ignore
from ..serializers.user_forgot_set_password import UserForgotSetPasswordSerializer #type: ignore

class UserForgotSetPasswordView(generics.GenericAPIView):
    serializer_class = UserForgotSetPasswordSerializer
    permission_classes = [permissions.AllowAny]  

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response({
            "message": "Password has been reset successfully.",
            "details": f"The password for {serializer.user.email} has been updated.",
        })