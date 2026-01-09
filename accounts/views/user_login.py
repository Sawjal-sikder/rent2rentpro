from rest_framework import generics # type: ignore
from ..serializers.user_login import UserLoginSerializer # type: ignore
from rest_framework_simplejwt.views import TokenObtainPairView # type: ignore

class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer