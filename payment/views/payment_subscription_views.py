import os
import stripe #type: ignore
from django.contrib.auth import get_user_model #type: ignore
from django.utils import timezone #type: ignore
from rest_framework import generics, permissions, status #type: ignore
from rest_framework.response import Response #type: ignore
from payment.models import PaymentPlan, Subscription
from payment.serializers.payment_subscription_serializer import PaymentSubscriptionSerializer

User = get_user_model()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


class PaymentSubscriptionViews(generics.CreateAPIView):
    serializer_class = PaymentSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        payment_plan_id = request.data.get('payment_plan_id')

        # Validate payment plan
        try:
            payment_plan = PaymentPlan.objects.get(id=payment_plan_id, is_active=True)
        except PaymentPlan.DoesNotExist:
            return Response({"message": "Invalid payment plan."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already has an active subscription
        active_subscription = Subscription.objects.filter(
            user=user, 
            status__in=['active', 'trialing']
        ).first()
        
        if active_subscription:
            return Response(
                {"message": "User already has an active subscription."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if stripe customer exists from previous subscription
        existing_subscription = Subscription.objects.filter(user=user).first()

        if existing_subscription and existing_subscription.stripe_customer_id:
            customer_id = existing_subscription.stripe_customer_id
        else:
            # Create new Stripe customer
            try:
                customer = stripe.Customer.create(
                    email=user.email,
                    name=user.full_name
                )
                customer_id = customer.id
            except stripe.error.StripeError as e:
                return Response(
                    {"error": f"Failed to create customer: {str(e)}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Build subscription parameters
        subscription_params = {
            'customer': customer_id,
            'items': [{'price': payment_plan.stripe_price_id}],
            'payment_behavior': 'default_incomplete',
            'expand': ['latest_invoice.payment_intent'],
        }
        
        # Add trial period if exists
        if payment_plan.trial_period_days:
            subscription_params['trial_period_days'] = payment_plan.trial_period_days

        # Create Stripe Subscription
        try:
            stripe_subscription = stripe.Subscription.create(**subscription_params)
        except stripe.error.StripeError as e:
            return Response(
                {"error": f"Failed to create subscription: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save Subscription in DB
        new_subscription = Subscription.objects.create(
            user=user,
            payment_plan=payment_plan,
            stripe_customer_id=customer_id,
            stripe_subscription_id=stripe_subscription['id'],
            status=stripe_subscription['status'],
            start_date=timezone.datetime.fromtimestamp(
                stripe_subscription['current_period_start'], 
                tz=timezone.utc
            ),
            end_date=timezone.datetime.fromtimestamp(
                stripe_subscription['current_period_end'], 
                tz=timezone.utc
            ),
            trial_start=timezone.datetime.fromtimestamp(
                stripe_subscription['trial_start'], 
                tz=timezone.utc
            ) if stripe_subscription.get('trial_start') else None,
            trial_end=timezone.datetime.fromtimestamp(
                stripe_subscription['trial_end'], 
                tz=timezone.utc
            ) if stripe_subscription.get('trial_end') else None,
        )

        serializer = self.get_serializer(new_subscription)
        
        # Include client_secret for frontend payment confirmation if needed
        response_data = serializer.data
        if stripe_subscription.get('latest_invoice') and stripe_subscription['latest_invoice'].get('payment_intent'):
            response_data['client_secret'] = stripe_subscription['latest_invoice']['payment_intent']['client_secret']

        return Response(response_data, status=status.HTTP_201_CREATED)