from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.permissions import AllowAny # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.utils.decorators import method_decorator # type: ignore
from datetime import timezone as dt_timezone
from django.utils import timezone # type: ignore
import logging
import stripe # type: ignore
import os

from payment.models import Subscription, PaymentPlan
from accounts.models import CustomUser

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class WebhookViews(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError as e:
            logger.error(f"Invalid payload: {str(e)}")
            return Response({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {str(e)}")
            return Response({'error': 'Invalid signature'}, status=400)

        event_type = event['type']
        data_object = event['data']['object']

        logger.info(f"Received webhook event: {event_type}")

        try:
            if event_type == 'checkout.session.completed':
                self.handle_checkout_session_completed(data_object)
            elif event_type == 'customer.subscription.updated':
                self.handle_subscription_updated(data_object)
            elif event_type == 'customer.subscription.deleted':
                self.handle_subscription_deleted(data_object)
            elif event_type == 'invoice.payment_succeeded':
                self.handle_invoice_payment_succeeded(data_object)
            elif event_type == 'invoice.payment_failed':
                self.handle_invoice_payment_failed(data_object)
            else:
                logger.info(f"Unhandled event type: {event_type}")
        except Exception as e:
            logger.error(f"Error handling {event_type}: {str(e)}")
            return Response({'error': str(e)}, status=500)

        return Response({'status': 'success'}, status=200)

    def handle_checkout_session_completed(self, session):
        """
        Handle checkout.session.completed event.
        The session object does NOT contain current_period_start/end.
        We need to retrieve the subscription separately.
        """
        logger.info("Processing checkout.session.completed")

        # Get subscription ID from the session
        subscription_id = session.get('subscription')
        customer_id = session.get('customer')
        
        # Get metadata
        metadata = session.get('metadata', {})
        user_id = metadata.get('user_id')
        payment_plan_id = metadata.get('payment_plan_id')

        if not subscription_id:
            logger.warning("No subscription_id in checkout session")
            return

        if not user_id:
            logger.warning("No user_id in session metadata")
            return

        try:
            # Retrieve the actual subscription from Stripe
            stripe_subscription = stripe.Subscription.retrieve(subscription_id)

            # Extract timestamps safely
            start_timestamp = stripe_subscription.get('current_period_start')
            end_timestamp = stripe_subscription.get('current_period_end')
            trial_start_timestamp = stripe_subscription.get('trial_start')
            trial_end_timestamp = stripe_subscription.get('trial_end')

            # First look for pending subscription by user_id
            subscription = Subscription.objects.filter(
                user_id=user_id,
                status='pending'
            ).first()

            # If not found, try by stripe_subscription_id (for edge cases)
            if not subscription:
                subscription = Subscription.objects.filter(
                    stripe_subscription_id=subscription_id
                ).first()

            if subscription:
                # Update existing subscription
                subscription.stripe_subscription_id = subscription_id
                subscription.stripe_customer_id = customer_id
                subscription.status = stripe_subscription['status']
                subscription.start_date = timezone.datetime.fromtimestamp(
                    start_timestamp, tz=dt_timezone.utc
                ) if start_timestamp else None
                subscription.end_date = timezone.datetime.fromtimestamp(
                    end_timestamp, tz=dt_timezone.utc
                ) if end_timestamp else None
                subscription.trial_start = timezone.datetime.fromtimestamp(
                    trial_start_timestamp, tz=dt_timezone.utc
                ) if trial_start_timestamp else None
                subscription.trial_end = timezone.datetime.fromtimestamp(
                    trial_end_timestamp, tz=dt_timezone.utc
                ) if trial_end_timestamp else None
                subscription.save()
                logger.info(f"Updated subscription for user {user_id}, stripe_sub_id: {subscription_id}, status: {stripe_subscription['status']}")
            else:
                # Create new if not found (fallback)
                user = CustomUser.objects.get(id=user_id)
                payment_plan = None
                if payment_plan_id:
                    payment_plan = PaymentPlan.objects.filter(id=payment_plan_id).first()

                subscription = Subscription.objects.create(
                    user=user,
                    payment_plan=payment_plan,
                    stripe_subscription_id=subscription_id,
                    stripe_customer_id=customer_id,
                    status=stripe_subscription['status'],
                    start_date=timezone.datetime.fromtimestamp(
                        start_timestamp, tz=dt_timezone.utc
                    ) if start_timestamp else None,
                    end_date=timezone.datetime.fromtimestamp(
                        end_timestamp, tz=dt_timezone.utc
                    ) if end_timestamp else None,
                    trial_start=timezone.datetime.fromtimestamp(
                        trial_start_timestamp, tz=dt_timezone.utc
                    ) if trial_start_timestamp else None,
                    trial_end=timezone.datetime.fromtimestamp(
                        trial_end_timestamp, tz=dt_timezone.utc
                    ) if trial_end_timestamp else None,
                )
                logger.info(f"Created new subscription for user {user_id}")

        except stripe.error.StripeError as e:
            logger.error(f"Stripe error retrieving subscription: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in checkout.session.completed: {str(e)}")
            raise

    def handle_subscription_updated(self, subscription):
        """Handle customer.subscription.updated event"""
        logger.info("Processing customer.subscription.updated")

        subscription_id = subscription['id']
        
        try:
            db_subscription = Subscription.objects.filter(
                stripe_subscription_id=subscription_id
            ).first()

            if db_subscription:
                start_timestamp = subscription.get('current_period_start')
                end_timestamp = subscription.get('current_period_end')

                db_subscription.status = subscription['status']
                db_subscription.start_date = timezone.datetime.fromtimestamp(
                    start_timestamp, tz=dt_timezone.utc
                ) if start_timestamp else db_subscription.start_date
                db_subscription.end_date = timezone.datetime.fromtimestamp(
                    end_timestamp, tz=dt_timezone.utc
                ) if end_timestamp else db_subscription.end_date
                db_subscription.save()
                logger.info(f"Updated subscription {subscription_id}")
            else:
                logger.warning(f"Subscription not found: {subscription_id}")

        except Exception as e:
            logger.error(f"Error updating subscription: {str(e)}")
            raise

    def handle_subscription_deleted(self, subscription):
        """Handle customer.subscription.deleted event"""
        logger.info("Processing customer.subscription.deleted")

        subscription_id = subscription['id']

        try:
            db_subscription = Subscription.objects.filter(
                stripe_subscription_id=subscription_id
            ).first()

            if db_subscription:
                db_subscription.status = 'canceled'
                db_subscription.canceled_at = timezone.now()
                db_subscription.save()
                logger.info(f"Canceled subscription {subscription_id}")
            else:
                logger.warning(f"Subscription not found: {subscription_id}")

        except Exception as e:
            logger.error(f"Error deleting subscription: {str(e)}")
            raise

    def handle_invoice_payment_succeeded(self, invoice):
        """Handle invoice.payment_succeeded event (renewals)"""
        logger.info("Processing invoice.payment_succeeded")

        subscription_id = invoice.get('subscription')
        if not subscription_id:
            return

        try:
            # Retrieve fresh subscription data
            stripe_subscription = stripe.Subscription.retrieve(subscription_id)

            db_subscription = Subscription.objects.filter(
                stripe_subscription_id=subscription_id
            ).first()

            if db_subscription:
                start_timestamp = stripe_subscription.get('current_period_start')
                end_timestamp = stripe_subscription.get('current_period_end')

                db_subscription.status = stripe_subscription['status']
                db_subscription.start_date = timezone.datetime.fromtimestamp(
                    start_timestamp, tz=dt_timezone.utc
                ) if start_timestamp else db_subscription.start_date
                db_subscription.end_date = timezone.datetime.fromtimestamp(
                    end_timestamp, tz=dt_timezone.utc
                ) if end_timestamp else db_subscription.end_date
                db_subscription.save()
                logger.info(f"Renewed subscription {subscription_id}")

        except Exception as e:
            logger.error(f"Error in payment succeeded: {str(e)}")
            raise

    def handle_invoice_payment_failed(self, invoice):
        """Handle invoice.payment_failed event"""
        logger.info("Processing invoice.payment_failed")

        subscription_id = invoice.get('subscription')
        if not subscription_id:
            return

        try:
            db_subscription = Subscription.objects.filter(
                stripe_subscription_id=subscription_id
            ).first()

            if db_subscription:
                db_subscription.status = 'past_due'
                db_subscription.save()
                logger.info(f"Marked subscription {subscription_id} as past_due")

        except Exception as e:
            logger.error(f"Error in payment failed: {str(e)}")
            raise