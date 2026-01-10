from rest_framework import generics #type: ignore
from rest_framework import permissions #type: ignore
from rest_framework.response import Response #type: ignore

class UserProfileDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({
            "message": "User profile deleted successfully.",
            "details": "Your user profile has been removed from the system.",
        })