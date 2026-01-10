from rest_framework import generics #type: ignore
from rest_framework import permissions #type: ignore
from rest_framework.response import Response #type: ignore
from rest_framework_simplejwt.tokens import RefreshToken #type: ignore
from ..serializers.user_registration_active import UserRegistrationActiveSerializer #type: ignore


class UserRegistrationActiveView(generics.GenericAPIView):
    serializer_class = UserRegistrationActiveSerializer
    permission_classes = [permissions.AllowAny]  

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "User account activated successfully.",
            "user_id": user.id,
            "email": user.email,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })