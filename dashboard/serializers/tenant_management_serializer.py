from rest_framework import serializers # type: ignore
from service.models import ContactCreationFile # type: ignore

class ContactCreationFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactCreationFile
        fields = ['id', 'title', 'file', 'created_at', 'updated_at']