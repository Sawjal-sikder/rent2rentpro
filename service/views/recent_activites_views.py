from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.models import (
    ContactCreationFile,
    EmailReplyDraft,
    ContractAnalysis,
    LocationSuitability,
)


class RecentActivitiesView(APIView):
    def get(self, request):
        user = request.user

        cf = ContactCreationFile.objects.filter(user=user).order_by('-created_at').first()
        ed = EmailReplyDraft.objects.filter(user=user).order_by('-created_at').first()
        ca = ContractAnalysis.objects.filter(user=user).order_by('-created_at').first()
        ls = LocationSuitability.objects.filter(user=user).order_by('-created_at').first()

        data = {
            "contact_creation_file": (
                {
                    "id": cf.id,
                    "title": cf.title,
                    "file_url": cf.file.url if cf.file else None,
                    "created_at": cf.created_at,
                }
                if cf else None
            ),
            "email_reply_draft": (
                {
                    "id": ed.id,
                    "generated_email_subject": ed.generated_email_subject,
                    "created_at": ed.created_at,
                }
                if ed else None
            ),
            "contract_analysis": (
                {
                    "id": ca.id,
                    "contract_file_url": ca.contract_file.url if ca.contract_file else None,
                    "created_at": ca.created_at,
                }
                if ca else None
            ),
            "location_suitability": (
                {
                    "id": ls.id,
                    "analysis_summary": ls.analysis_summary,
                    "created_at": ls.created_at,
                }
                if ls else None
            ),
        }

        return Response(data, status=status.HTTP_200_OK)
