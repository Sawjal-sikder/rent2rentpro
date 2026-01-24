from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from service.models import (
    ContactCreationFile,
    EmailReplyDraft,
    ContractAnalysis,
    LocationSuitability,
)
from service.serializers.recent_activites_serializer import ContactCreationFileSerializer, ContractAnalysisSerializer, EmailReplyDraftSerializer, LocationSuitabilitySerializer



class RecentActivitiesView(APIView):
    def get(self, request):
        user = request.user

        cf = ContactCreationFile.objects.filter(user=user).order_by('-created_at').first()
        ed = EmailReplyDraft.objects.filter(user=user).order_by('-created_at').first()
        ca = ContractAnalysis.objects.filter(user=user).order_by('-created_at').first()
        ls = LocationSuitability.objects.filter(user=user).order_by('-created_at').first()

        data = {
            "contact_creation_file": ContactCreationFileSerializer(cf).data if cf else None,
            "email_reply_draft": EmailReplyDraftSerializer(ed).data if ed else None,
            "contract_analysis": ContractAnalysisSerializer(ca).data if ca else None,
            "location_suitability": LocationSuitabilitySerializer(ls).data if ls else None,
        }

        return Response(data, status=status.HTTP_200_OK)
