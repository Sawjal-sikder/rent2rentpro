from rest_framework import serializers # type: ignore
from django.contrib.auth import get_user_model # type: ignore
User = get_user_model()


class UserProfileChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if not self.context['request'].user.check_password(data['old_password']):
            raise serializers.ValidationError({"message": "Old password is incorrect."})
        
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({"message": "New password must be different from the old password."})
        
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"message": "New password and confirm new password do not match."})
        return data
    
    def validate_new_password(self, value):
        # Add custom password validation logic here if needed
        if len(value) < 8:
            raise serializers.ValidationError("New password must be at least 8 characters long.")
        return value
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
    