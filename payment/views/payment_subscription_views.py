import os
from datetime import timezone as dt_timezone
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
        BASE_URL_FRONTEND = os.getenv('BASE_URL_FRONTEND', 'https://www.google.com')

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

        try:
            # Check if stripe customer exists from previous subscription
            existing_subscription = Subscription.objects.filter(user=user).first()

            if existing_subscription and existing_subscription.stripe_customer_id:
                customer_id = existing_subscription.stripe_customer_id
            else:
                customer = stripe.Customer.create(
                    email=user.email,
                    name=user.full_name
                )
                customer_id = customer.id

            # Create checkout session
            checkout_session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': payment_plan.stripe_price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=BASE_URL_FRONTEND,
                cancel_url=BASE_URL_FRONTEND,
                subscription_data={
                    'trial_period_days': payment_plan.trial_period_days if payment_plan.trial_period_days else None,
                    'metadata': {
                        'user_id': str(user.id),
                        'payment_plan_id': str(payment_plan.id),
                        'type': 'subscription',
                    }
                },
                metadata={
                    'user_id': str(user.id),
                    'payment_plan_id': str(payment_plan.id),
                    'type': 'subscription',
                },
                automatic_tax={'enabled': False},
                allow_promotion_codes=False,
            )
            
            # Save pending subscription to DB
            subscription = Subscription.objects.create(
                user=user,
                payment_plan=payment_plan,
                stripe_customer_id=customer_id,
                stripe_subscription_id=None,
                status='pending',
            )
            
            return Response(
                {
                    'checkout_session_id': checkout_session.id,
                    'checkout_session_url': checkout_session.url,
                    'subscription_id': subscription.id,
                    'subscription_plan': payment_plan.name,
                    'trial_period_days': payment_plan.trial_period_days if payment_plan.trial_period_days else None,
                },
                status=status.HTTP_201_CREATED
            )
        
        except stripe.error.StripeError as e:
            return Response(
                {"error": f"Stripe error: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )