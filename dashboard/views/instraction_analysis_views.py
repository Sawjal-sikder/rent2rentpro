from rest_framework import generics, permissions, response # type: ignore
from django.http import Http404 # type: ignore
from service.models import InstractionAnalysis # type: ignore
from dashboard.serializers.instraction_analysis_serializer import InstractionAnalysisSerializer # type: ignore

class InstractionAnalysisView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = InstractionAnalysisSerializer

    def get_object(self):
        obj = InstractionAnalysis.objects.first()
        
        if obj is None:
            obj = InstractionAnalysis.objects.create(
                rules_contract_createion="demo rules_contract_createion",
                rules_email_reply="demo rules_email_reply",
                rules_location_suitability="demo rules_location_suitability",
                rules_contract_analysis="demo rules_contract_analysis",
            )
        
        return obj
    
    
class InstractionAnalysisUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = InstractionAnalysisSerializer
    queryset = InstractionAnalysis.objects.all()
    
    def get_object(self):
        # Get the first record (no ID needed)
        obj = InstractionAnalysis.objects.first()
        if obj is None:
            raise Http404("No InstractionAnalysis found")
        return obj
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response({
            "message": "Instraction Analysis updated successfully",
            "instraction_analysis": serializer.data
        })