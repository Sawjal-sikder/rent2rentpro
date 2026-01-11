from rest_framework import generics # type: ignore
from rest_framework import permissions # type: ignore
from ..serializers.user_profile_update import (
    UserCompanyProfileSerializer,
    UserIndivisualProfileSerializer
)

class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        if user.user_type == 'company':
            return UserCompanyProfileSerializer
        else:
            return UserIndivisualProfileSerializer

    def get_object(self):
        return self.request.user