import os #type: ignore
import stripe #type: ignore
from django.contrib.auth import get_user_model #type: ignore
User = get_user_model()
from rest_framework import generics, permissions, status #type: ignore
from rest_framework.response import Response #type: ignore
from payment.models import PaymentPlan, Subscription
from datetime import datetime #type: ignore
from payment.serializers.payment_subscription_serializer import PaymentSubscriptionSerializer

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


class PaymentSubscriptionViews(generics.CreateAPIView):
    serializer_class = PaymentSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        payment_plan_id = request.data.get('payment_plan_id')

        try:
            payment_plan = PaymentPlan.objects.get(id=payment_plan_id, is_active=True)
        except PaymentPlan.DoesNotExist:
            return Response({"error": "Invalid payment plan."}, status=status.HTTP_400_BAD_REQUEST)

        # Create Stripe Customer if not exists
        if not user.stripe_customer_id:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.full_name
            )
            user.stripe_customer_id = customer['id']
            user.save()

        # Create Stripe Subscription
        try:
            subscription = stripe.Subscription.create(
                customer=user.stripe_customer_id,
                items=[{'price': payment_plan.stripe_price_id}],
                trial_period_days=payment_plan.trial_period_days
            )
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Save Subscription in DB
        new_subscription = Subscription.objects.create(
            user=user,
            payment_plan=payment_plan,
            stripe_customer_id=user.stripe_customer_id,
            stripe_subscription_id=subscription['id'],
            status=subscription['status'],
            start_date=datetime.fromtimestamp(subscription['current_period_start']),
            end_date=datetime.fromtimestamp(subscription['current_period_end']),
            trial_start=datetime.fromtimestamp(subscription['trial_start']) if subscription['trial_start'] else None,
            trial_end=datetime.fromtimestamp(subscription['trial_end']) if subscription['trial_end'] else None,
        )

        serializer = self.get_serializer(new_subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)