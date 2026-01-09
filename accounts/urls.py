from django.urls import path # type: ignore
from .views import user_registration, user_login # type: ignore

urlpatterns = [
    path('register/', user_registration.UserRegistrationView.as_view(), name='user-registration'),
    path('login/', user_login.UserLoginView.as_view(), name='user-login'),
]