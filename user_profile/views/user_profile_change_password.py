from rest_framework import generics #type: ignore
from rest_framework import permissions #type: ignore
from rest_framework.response import Response #type: ignore
from ..serializers.user_profile_change_password import UserProfileChangePasswordSerializer #type: ignore

class UserProfileChangePasswordView(generics.GenericAPIView):
    serializer_class = UserProfileChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "message": "Password changed successfully.",
            "details": "Your password has been updated.",
        })
