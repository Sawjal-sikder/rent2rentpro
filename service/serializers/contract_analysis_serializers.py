from rest_framework import serializers #type: ignore
from service.models import ContractAnalysis

class ContractAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractAnalysis
        fields = [
            'id',
            'user',
            'contract_file',
            'contract_analysis_result',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'contract_analysis_result', 'created_at', 'updated_at']