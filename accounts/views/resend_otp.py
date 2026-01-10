from rest_framework import generics #type: ignore
from rest_framework import permissions #type: ignore
from rest_framework.response import Response #type: ignore
from ..serializers.resend_otp import ResendOTPSerializer #type: ignore

class ResendOTPView(generics.GenericAPIView):
    serializer_class = ResendOTPSerializer
    permission_classes = [permissions.AllowAny]  

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            "message": "OTP resent successfully.",
            "details": f"Please check your email ({user.email}) for the new OTP code."
        })