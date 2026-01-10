from django.urls import path # type: ignore

from .views import (
    user_profile_details,
    ) # type: ignore

urlpatterns = [
    # User Profile Details
    path('profile/details/', user_profile_details.UserProfileDetailsView.as_view(), name='user-profile-details'),
]