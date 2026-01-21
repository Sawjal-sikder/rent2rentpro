from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # type: ignore
from payment.models import Subscription
from django.utils import timezone # type: ignore


class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        return {
            "message": "Login successful",
            "user_details": {
                "email": self.user.email,
                "full_name": self.user.full_name,
                "phone_number": self.user.phone_number,
                "is_premium": self.check_premium_status(self.user),
                "user_role": self.get_user_role(self.user),
            },
            "refresh": data['refresh'],
            "access": data['access'],
        }

    def check_premium_status(self, user):
        subscription = Subscription.objects.filter(
            user=user
        ).order_by('-created_at').first()

        if not subscription:
            return False

        if subscription.status not in ['active', 'trialing']:
            return False

        if subscription.status == 'trialing':
            return True

        if subscription.end_date and subscription.end_date > timezone.now():
            return True

        return False
    
    def get_user_role(self, user):
        if user.is_active and user.is_staff and user.is_superuser:
            return "superadmin"
        
        elif user.is_active and user.is_staff:
            return "admin"
        
        elif user.is_active:
            return "user"