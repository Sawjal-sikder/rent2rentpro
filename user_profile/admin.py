from django.contrib import admin # type: ignore
from .models import Feedback # type: ignore

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__email', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)