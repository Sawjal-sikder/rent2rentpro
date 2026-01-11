from rest_framework import permissions, response, generics #type: ignore
from ..serializers.user_feedback import UserFeedbackSerializer
from ..models import Feedback

class UserFeedbackCreateListView(generics.ListCreateAPIView):
    serializer_class = UserFeedbackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Feedback.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return response.Response(
            {"detail": "Feedback created successfully.", "data": serializer.data},
            status=201
        )