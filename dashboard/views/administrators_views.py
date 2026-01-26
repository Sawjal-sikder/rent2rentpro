from rest_framework import generics, permissions, response, status # type: ignore  
from dashboard.serializers.administrators_serializer import AdministratorsSerializer # type: ignore
from dashboard.views.pagination_views import SetPagination # type: ignore
from django.contrib.auth import get_user_model # type: ignore
User = get_user_model()

class AdministratorsView(generics.ListAPIView):
    queryset = User.objects.filter(is_staff=True).order_by('-id')
    serializer_class = AdministratorsSerializer
    permission_classes = [permissions.IsAdminUser]    
    pagination_class = SetPagination
    
    
class AdministratorsCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdministratorsSerializer
    
    def perform_create(self, serializer):
        password = serializer.validated_data.pop('password', None)
        role = serializer.validated_data.pop('role', 'admin').lower()
        
        if role not in ['admin', 'superadmin']:
            role = 'admin' 
        
        instance = serializer.save(
            is_staff=True,
            is_superuser=(role == 'superadmin')  # True only for superadmin, False for admin
        )
            
        if password:
            instance.set_password(password)
            instance.save(update_fields=['password'])
            
            
class AdministratorsdetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_staff=True)
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdministratorsSerializer
    lookup_field = 'id'
    
    def perform_update(self, serializer):
        password = serializer.validated_data.pop('password', None)
        role = serializer.validated_data.pop('role', '').lower()
        
        # Prepare update data
        update_data = {'is_staff': True}
        
        if role == 'superadmin':
            update_data['is_superuser'] = True
        elif role == 'admin':
            update_data['is_superuser'] = False
        
        instance = serializer.save(**update_data)
            
        # Handle password update
        if password:
            instance.set_password(password)
            instance.save(update_fields=['password'])
            
    def destroy(self, request, *args, **kwargs):
        admin = self.get_object()
        admin.delete()
        return response.Response({
                "message": "Administrator deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)