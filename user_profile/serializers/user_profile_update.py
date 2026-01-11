from rest_framework import serializers #type: ignore
from django.contrib.auth import get_user_model #type: ignore
User = get_user_model()


class UserCompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['company_name', 'email', 'company_address', 'company_vat_number']
        
        
class UserIndivisualProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'address', 'profile_image']