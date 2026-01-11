from rest_framework import serializers #type: ignore
from ..models import Feedback

class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"
        read_only_fields = ("id", "user", "created_at")
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_information'] = {
            "id": instance.user.id,
            "full_name": instance.user.full_name,
            "email": instance.user.email,
        }
        return representation