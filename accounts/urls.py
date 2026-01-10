from django.urls import path # type: ignore
from .views import user_registration, user_login, user_registration_active, resend_otp # type: ignore

urlpatterns = [
    path('register/', user_registration.UserRegistrationView.as_view(), name='user-registration'),
    path('register/activate/', user_registration_active.UserRegistrationActiveView.as_view(), name='user-registration-activate'),
    path('resend-otp/', resend_otp.ResendOTPView.as_view(), name='resend-otp'),
    path('login/', user_login.UserLoginView.as_view(), name='user-login'),
]