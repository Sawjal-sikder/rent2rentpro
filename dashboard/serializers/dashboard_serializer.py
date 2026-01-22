from rest_framework import serializers # type: ignore
from django.contrib.auth import get_user_model # type: ignore
User = get_user_model()

class DashboardSerializer(serializers.Serializer):
    
    def to_representation(self, instance):
        return {
            "total_users": User.objects.count(),
            "active_users": User.objects.filter(is_active=True).count(),
            'individual_users': User.objects.filter(user_type='individual').count(),
            'company_users': User.objects.filter(user_type='company').count(),
        }