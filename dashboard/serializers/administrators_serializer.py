from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class AdministratorsSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone_number', 'role', 'password']
        extra_kwargs = {
            'full_name': {'required': False},
            'email': {'required': False},
            'phone_number': {'required': False},
        }
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if instance.is_staff and instance.is_superuser:
            representation['role'] = 'Super Admin'
        elif instance.is_staff:
            representation['role'] = 'Admin'
        else:
            representation['role'] = 'User'
        
        return representation