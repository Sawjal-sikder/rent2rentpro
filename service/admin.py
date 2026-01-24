from django.contrib import admin
from service.models import ContactCreationFile, EmailReplyDraft, ContractAnalysis, LocationSuitability

# Register your models here.

@admin.register(ContactCreationFile)
class ContactCreationFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'created_at', 'updated_at']
    search_fields = ['title', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
