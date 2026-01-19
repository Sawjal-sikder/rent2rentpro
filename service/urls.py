
from django.urls import path # type: ignore
from service.views.contact_cration_views import ContactCreationView
from service.views.email_reply_draft_views import EmailReplyDraftView
from service.views.contract_analysis_views import ContractAnalysisView, ContractAnalysisDetailView

urlpatterns = [
    path('contact-creation/', ContactCreationView.as_view(), name='contact-creation'),
    path('email-reply-draft/', EmailReplyDraftView.as_view(), name='email-reply-draft'),
    path('contract-analysis/', ContractAnalysisView.as_view(), name='contract-analysis'),
    path('contract-analysis/<int:pk>/', ContractAnalysisDetailView.as_view(), name='contract-analysis-detail'),
]