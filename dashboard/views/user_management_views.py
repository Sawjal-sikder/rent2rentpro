from rest_framework import generics, permissions, response, status, filters  # type: ignore
from dashboard.serializers.user_management_serializer import UserManagementSerializer # type: ignore
from dashboard.views.pagination_views import SetPagination # type: ignore
from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from django.contrib.auth import get_user_model # type: ignore
User = get_user_model()

class UserManagementView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserManagementSerializer
    
    pagination_class = SetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_type']
    search_fields = ['full_name', 'email', 'phone_number']
    
    def get_queryset(self):
        return User.objects.filter(is_staff=False, is_superuser=False).order_by('-id')
    
    
class UserToggleActiveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserManagementSerializer
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        serializer = self.get_serializer(user)
        return response.Response({
                "message": "User status updated successfully", 
                "user": serializer.data
        })
        
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return response.Response({
                "message": "User deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)