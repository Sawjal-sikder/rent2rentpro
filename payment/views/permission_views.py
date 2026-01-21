from rest_framework import permissions #type: ignore
from rest_framework.exceptions import APIException #type: ignore
from rest_framework import status #type: ignore
from payment.models import Subscription 
from django.utils import timezone #type: ignore


class SubscriptionRequired(APIException):
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = "Please purchase a subscription."
    default_code = "subscription_required"


class HasActiveSubscription(permissions.BasePermission):
    """
    Allows access only to users with active or trialing subscription.
    """

    message = "Please purchase a subscription."

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        subscription = Subscription.objects.filter(
            user=user
        ).order_by('-created_at').first()

        if not subscription:
            raise SubscriptionRequired()

        # Check if subscription status is valid
        if subscription.status not in ['active', 'trialing']:
            raise SubscriptionRequired()

        # Trialing without end_date is still valid
        if subscription.status == 'trialing':
            return True

        # For active subscriptions, check end_date
        if subscription.end_date and subscription.end_date > timezone.now():
            return True

        raise SubscriptionRequired()