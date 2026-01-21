from rest_framework import generics, permissions, response # type: ignore
from user_profile.serializers.user_feedback import UserFeedbackSerializer # type: ignore
from user_profile.models import Feedback # type: ignore
from dashboard.views.pagination_views import SetPagination # type: ignore


class UserFeedbackView(generics.ListAPIView):
    queryset = Feedback.objects.all().order_by('-created_at')
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserFeedbackSerializer
    pagination_class = SetPagination