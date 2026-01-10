from rest_framework import generics # type: ignore
from rest_framework import permissions # type: ignore
from ..serializers.user_profile_details import UserProfileDetailsSerializer


class UserProfileDetailsView(generics.RetrieveAPIView):
    serializer_class = UserProfileDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]  
    
    def get_object(self):
        return self.request.user