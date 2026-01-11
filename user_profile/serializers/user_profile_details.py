from rest_framework import serializers # type: ignore
from django.contrib.auth import get_user_model # type: ignore
User = get_user_model()

class UserProfileDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile details.
    """

    class Meta:
        model = User
        fields = ['id', 'user_type', 'email', 'full_name', 'phone_number', 'profile_image', 'is_active', 'address', 'company_name', 'company_address', 'company_vat_number']
        read_only_fields = ('id', 'user_type', 'email', 'full_name', 'phone_number', 'profile_image', 'is_active', 'address', 'company_name', 'company_address', 'company_vat_number')