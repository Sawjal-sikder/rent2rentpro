from rest_framework import serializers # type: ignore
from django.contrib.auth import get_user_model # type: ignore
User = get_user_model()

class AdministratorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone_number']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if instance.is_staff and instance.is_superuser:
            representation['role'] = 'Super Admin'
        
        elif instance.is_staff:
            representation['role'] = 'Admin'
        
        else:
            representation['role'] = 'User'
        
        return representation