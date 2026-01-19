from django.db import models # type: ignore
from django.contrib.auth import get_user_model # type: ignore
User = get_user_model()

class ContactCreationFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='contracts/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
    
class EmailReplyDraft(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_email_body = models.TextField()
    reply_guidance = models.TextField()
    generated_email_subject = models.CharField(max_length=255)
    generated_email_body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.generated_email_subject
    
    
class ContractAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contract_file = models.FileField(upload_to='contract_analyses/')
    contract_analysis_result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analysis for {self.contract_file.name} by {self.user.full_name}"