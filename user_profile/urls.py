from django.urls import path # type: ignore

from .views import (
    user_profile_details,
    user_profile_change_password,
    user_profile_delete,
    ) # type: ignore

urlpatterns = [
    # User Profile Details
    path('profile/details/', user_profile_details.UserProfileDetailsView.as_view(), name='user-profile-details'),
    # User Profile Change Password
    path('profile/change-password/', user_profile_change_password.UserProfileChangePasswordView.as_view(), name='user-profile-change-password'),
    # User Profile Delete
    path('profile/delete/', user_profile_delete.UserProfileDeleteView.as_view(), name='user-profile-delete'),
]