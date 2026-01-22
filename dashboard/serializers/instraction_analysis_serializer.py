from rest_framework import serializers # type: ignore
from service.models import InstractionAnalysis # type: ignore

class InstractionAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstractionAnalysis
        fields = '__all__'