from rest_framework import serializers
from service.models import (
    ContactCreationFile,
    EmailReplyDraft,
    ContractAnalysis,
    LocationSuitability,
)


class ContactCreationFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactCreationFile
        fields = "__all__"


class EmailReplyDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailReplyDraft
        fields = "__all__"


class ContractAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractAnalysis
        fields = "__all__"


class LocationSuitabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationSuitability
        fields = "__all__"
