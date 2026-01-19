from rest_framework import serializers #type: ignore
from service.models import EmailReplyDraft

class EmailReplyDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailReplyDraft
        fields = [
            'id',
            'user',
            'original_email_body',
            'reply_guidance',
            'generated_email_subject',
            'generated_email_body',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id','user','generated_email_subject', 'generated_email_body', 'created_at', 'updated_at']