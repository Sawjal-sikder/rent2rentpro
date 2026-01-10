from rest_framework import serializers # type: ignore
from django.contrib.auth import get_user_model # type: ignore
User = get_user_model()

class UserProfileDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile details.
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'profile_image', 'is_active']
        read_only_fields = ('id', 'email', 'full_name', 'phone_number', 'profile_image', 'is_active')