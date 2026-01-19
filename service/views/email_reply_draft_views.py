from rest_framework import generics, permissions, status, response #type: ignore
from service.models import EmailReplyDraft
from service.serializers.email_reply_draft_serializers import EmailReplyDraftSerializer
from service.utils.agent_request import make_agent_request
import os

class EmailReplyDraftView(generics.ListCreateAPIView):
    queryset = EmailReplyDraft.objects.all()
    serializer_class = EmailReplyDraftSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        original_email_body = serializer.validated_data['original_email_body']
        reply_guidance = serializer.validated_data['reply_guidance']
        
        if not original_email_body or not reply_guidance:
            return response.Response(
                {"detail": "Both 'original_email_body' and 'reply_guidance' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        agent_payload = {
            "user_email": original_email_body,
            "user_instruction": reply_guidance,
        }

        agent_response = make_agent_request(os.getenv("BASE_URL_AI_SERVICE") + "/ai/generate-message", agent_payload)

        if "error" in agent_response:
            return response.Response(
                {"detail": "Failed to generate email reply."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        message = agent_response.get("generated_message", {})
        response_data = message.get("response", {})

        generated_subject = response_data.get("subject", "")
        generated_body = response_data.get("body", "")
        

        email_reply_draft = EmailReplyDraft.objects.create(
            user = request.user,
            original_email_body=original_email_body,
            reply_guidance=reply_guidance,
            generated_email_subject=generated_subject,
            generated_email_body=generated_body
        )

        output_serializer = self.get_serializer(email_reply_draft)
        return response.Response(output_serializer.data, status=status.HTTP_201_CREATED)