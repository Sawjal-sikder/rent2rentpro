from django.urls import path # type: ignore
from dashboard.views.user_management_views import (
    UserManagementView,
    UserToggleActiveView,
)

urlpatterns = [
    path('user-management/', UserManagementView.as_view(), name='user-management'),
    path('user-management/toggle-active/<int:id>/', UserToggleActiveView.as_view(), name='user-toggle-active'),
]