from payment.views.permission_views import HasActiveSubscription
from rest_framework import generics, permissions, response, status #type: ignore
from service.models import ContractAnalysis
from service.serializers.contract_analysis_serializers import ContractAnalysisSerializer
from service.utils.agent_request import make_file_request
import os
from django.urls import reverse # type: ignore  

class ContractAnalysisView(generics.ListCreateAPIView):
    queryset = ContractAnalysis.objects.all()
    serializer_class = ContractAnalysisSerializer
    permission_classes = [HasActiveSubscription]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        contract_file = serializer.validated_data['contract_file']

        if not contract_file:
            return response.Response(
                {"detail": "'contract_file' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save ContractAnalysis object first (without analysis result)
        contract_analysis = ContractAnalysis.objects.create(
            user=request.user,
            contract_file=contract_file,
            contract_analysis_result={}  # Empty for now
        )
        
        print("-----------------------------------------------------")
        print(f"url: {os.getenv('BASE_URL_AI_SERVICE') + '/ai/analyze_file'}")

        # Pass the file path to Celery task
        task = make_file_request.delay(
            url=os.getenv("BASE_URL_AI_SERVICE") + "/ai/analyze_file",
            file_path=contract_analysis.contract_file.path,  # File path on disk
            contract_analysis_id=contract_analysis.id
        )
        
        detail_url = request.build_absolute_uri(
            reverse('contract-analysis-detail', kwargs={'pk': contract_analysis.id})
        )

        # Return immediately (async processing)
        output_serializer = self.get_serializer(contract_analysis)
        return response.Response(
            {
                **output_serializer.data,
                "task_id": task.id,
                "status": "processing",
                "redirect_url": detail_url
            },
            status=status.HTTP_202_ACCEPTED
        )
        
        
class ContractAnalysisDetailView(generics.RetrieveAPIView):
    queryset = ContractAnalysis.objects.all()
    serializer_class = ContractAnalysisSerializer
    permission_classes = [HasActiveSubscription]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)