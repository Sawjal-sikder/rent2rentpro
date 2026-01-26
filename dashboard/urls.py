from django.urls import path # type: ignore
from dashboard.views.instraction_analysis_views import InstractionAnalysisView, InstractionAnalysisUpdateView
from dashboard.views.dashboard_views import DashboardView, UserInsightsView
from dashboard.views.user_feedback_views import UserFeedbackView

from dashboard.views.administrators_views import (
    AdministratorsView,
    AdministratorsCreateView,
    AdministratorsdetailView,
)
from dashboard.views.user_management_views import (
    UserManagementView,
    UserToggleActiveView,
    UserUpdateView,
)
from dashboard.views.tenant_management_views import (
    TenantManagementView,
)

urlpatterns = [
    path('user-management/', UserManagementView.as_view(), name='user-management'),
    path('user-management/toggle-active/<int:id>/', UserToggleActiveView.as_view(), name='user-toggle-active'),
    path('user-management/<int:id>/', UserUpdateView.as_view(), name='user-update'),
    
    # administrators view can be added here when needed
    path('administrators/', AdministratorsView.as_view(), name='administrators'),
    path('administrators/create/', AdministratorsCreateView.as_view(), name='administrators-create'),
    path('administrators/<int:id>/', AdministratorsdetailView.as_view(), name='administrators-detail'),
    
    # tenant management
    path('tenant-management/', TenantManagementView.as_view(), name='tenant-management'),
    
    # user feedback can be added here when needed
    path('user-feedback/', UserFeedbackView.as_view(), name='user-feedback'),
    
    # dashboard/urls.py
    path('overview/', DashboardView.as_view(), name='dashboard-overview'),
    path('user-insights/', UserInsightsView.as_view(), name='user-insights'),
    path('analysis-rules/', InstractionAnalysisView.as_view(), name='analysis-rules'),
    path('analysis-rules/update/', InstractionAnalysisUpdateView.as_view(), name='analysis-rules-update'),
    
]