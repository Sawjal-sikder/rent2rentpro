from django.urls import path # type: ignore
from .views import (
    user_registration, 
    user_login, 
    user_registration_active, 
    resend_otp, 
    user_forgot_password, 
    user_forgot_password_verification, 
    user_forgot_set_password,
    user_profile_details,
) # type: ignore

urlpatterns = [
    # Registration URLs
    path('register/', user_registration.UserRegistrationView.as_view(), name='user-registration'),
    path('register/activate/', user_registration_active.UserRegistrationActiveView.as_view(), name='user-registration-activate'),
    path('resend-otp/', resend_otp.ResendOTPView.as_view(), name='resend-otp'),
    # Login URL
    path('login/', user_login.UserLoginView.as_view(), name='user-login'),
    # forgot password URL
    path('forgot-password/', user_forgot_password.UserForgotPasswordView.as_view(), name='user-forgot-password'),
    path('forgot-password/verify/', user_forgot_password_verification.UserForgotPasswordVerificationView.as_view(), name='user-forgot-password-verify'),
    path('forgot-password/set/password/', user_forgot_set_password.UserForgotSetPasswordView.as_view(), name='user-forgot-set-password'),
    # User Profile Details
    path('profile/details/', user_profile_details.UserProfileDetailsView.as_view(), name='user-profile-details'),
]