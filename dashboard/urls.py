from django.urls import path # type: ignore
from dashboard.views.administrators_views import (
    AdministratorsView,
    AdministratorsCreateView,
    AdministratorsdetailView,
)

from dashboard.views.user_management_views import (
    UserManagementView,
    UserToggleActiveView,
)
from dashboard.views.tenant_management_views import (
    TenantManagementView,
)

urlpatterns = [
    path('user-management/', UserManagementView.as_view(), name='user-management'),
    path('user-management/toggle-active/<int:id>/', UserToggleActiveView.as_view(), name='user-toggle-active'),
    
    # administrators view can be added here when needed
    path('administrators/', AdministratorsView.as_view(), name='administrators'),
    path('administrators/create/', AdministratorsCreateView.as_view(), name='administrators-create'),
    path('administrators/<int:id>/', AdministratorsdetailView.as_view(), name='administrators-detail'),
    
    # tenant management
    path('tenant-management/', TenantManagementView.as_view(), name='tenant-management'),
]