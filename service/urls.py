
from django.urls import path # type: ignore
from service.views.contact_cration_views import ContactCreationFileListView, ContactCreationView
from service.views.email_reply_draft_views import EmailReplyDraftView
from service.views.contract_analysis_views import ContractAnalysisView, ContractAnalysisDetailView
from service.views.location_suitability_views import LocationSuitabilityView, LocationSuitabilityDetailView

urlpatterns = [
    path('contact-creation/', ContactCreationView.as_view(), name='contact-creation'),
    path('contact-creation/files/', ContactCreationFileListView.as_view(), name='contact-creation-files'),
    path('email-reply-draft/', EmailReplyDraftView.as_view(), name='email-reply-draft'),
    path('contract-analysis/', ContractAnalysisView.as_view(), name='contract-analysis'),
    path('contract-analysis/<int:pk>/', ContractAnalysisDetailView.as_view(), name='contract-analysis-detail'),
    path('location-suitability/', LocationSuitabilityView.as_view(), name='location-suitability'),
    path('location-suitability/<int:pk>/', LocationSuitabilityDetailView.as_view(), name='location-suitability-detail'),
]