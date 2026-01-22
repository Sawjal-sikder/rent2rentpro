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
    
    
class LocationSuitability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city_size = models.CharField(max_length=255)
    district_type = models.CharField(max_length=255)
    demand_profile = models.CharField(max_length=255)
    public_transport = models.CharField(max_length=255)
    supermarkets_restaurants = models.CharField(max_length=255)
    universities_hospitals_offices = models.CharField(max_length=255)
    local_demand = models.CharField(max_length=255)
    competition_level = models.CharField(max_length=255)
    short_term_prices = models.CharField(max_length=255)
    regulatory_friendliness = models.CharField(max_length=255)
    analysis_summary = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Suitability Report for {self.user.full_name}"
    
    

class InstractionAnalysis(models.Model):
    rules_contract_createion = models.TextField()
    rules_email_reply = models.TextField()
    rules_location_suitability = models.TextField()
    rules_contract_analysis = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "Instruction Analysis Settings"