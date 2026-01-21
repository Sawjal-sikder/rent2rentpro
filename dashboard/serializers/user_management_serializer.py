from django.contrib.auth import get_user_model # type: ignore
from rest_framework import serializers # type: ignore
User = get_user_model()

class UserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email','phone_number', 'user_type', 'is_active']
