from rest_framework import generics, permissions, response # type: ignore
from payment.models import PaymentPlan
from payment.serializers.pyment_plan_serializers import PaymentPlanSerializer

import os #type: ignore
import stripe #type: ignore
from rest_framework import status, response #type: ignore

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')



class PaymentPlanListView(generics.ListAPIView):
    """
    API view to retrieve a list of all available payment plans.
    """
    queryset = PaymentPlan.objects.filter(is_active=True)
    serializer_class = PaymentPlanSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to list payment plans.
        """
        return self.list(request, *args, **kwargs)
    
    
class PaymentPlanCreateView(generics.CreateAPIView):
    """
    API view to create a new payment plan.
    """
    queryset = PaymentPlan.objects.all()
    serializer_class = PaymentPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        amount = request.data.get('amount')
        interval = request.data.get('interval')
        currency = request.data.get('currency', 'usd')
        trial_period_days = request.data.get('trial_period_days', 0)    
        
        if not all([name, amount, interval]):
            return response.Response(
                {"error": "Name, amount, and interval are required."},
                status=400
            )
        
        try:
            # Create Stripe Product
            product = stripe.Product.create(name=name)
            
            # Create Stripe Price
            price = stripe.Price.create(
                unit_amount=int(float(amount) * 100),  # amount in cents
                currency=currency,
                recurring={"interval": interval},
                product=product.id,
            )
            
            # Create PaymentPlan in the database
            payment_plan = PaymentPlan.objects.create(
                name=name,
                stripe_product_id=product.id,
                stripe_price_id=price.id,
                amount=amount,
                interval=interval,
                currency=currency,
                trial_period_days=trial_period_days,
                is_active=True
            )
            
            serializer = self.get_serializer(payment_plan)
            return response.Response(serializer.data, status=201)
        except Exception as e:
            return response.Response(
                {"error": str(e)},
                status=400
            )
        
            
class PaymentPlanUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing payment plan.
    """
    queryset = PaymentPlan.objects.all()
    serializer_class = PaymentPlanSerializer
    permission_classes = [permissions.IsAuthenticated]


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        name = request.data.get('name', instance.name)
        amount = request.data.get('amount', instance.amount)
        interval = request.data.get('interval', instance.interval)
        currency = request.data.get('currency', instance.currency)
        trial_period_days = request.data.get('trial_period_days', instance.trial_period_days)
        is_active = request.data.get('is_active', instance.is_active)
        
        try:
            # Update Stripe Product name if changed
            if name != instance.name:
                stripe.Product.modify(
                    instance.stripe_product_id,
                    name=name
                )
            
            # Check if price-related fields changed
            # Stripe doesn't allow updating price, so we need to create a new one
            price_changed = (
                float(amount) != float(instance.amount) or
                interval != instance.interval or
                currency != instance.currency
            )
            
            new_stripe_price_id = instance.stripe_price_id
            
            if price_changed:
                # Archive the old price
                stripe.Price.modify(
                    instance.stripe_price_id,
                    active=False
                )
                
                # Create new Stripe Price
                new_price = stripe.Price.create(
                    unit_amount=int(float(amount) * 100),
                    currency=currency,
                    recurring={"interval": interval},
                    product=instance.stripe_product_id,
                )
                new_stripe_price_id = new_price.id
            
            # Update product active status in Stripe
            if is_active != instance.is_active:
                stripe.Product.modify(
                    instance.stripe_product_id,
                    active=is_active
                )
            
            # Update local database
            instance.name = name
            instance.amount = amount
            instance.interval = interval
            instance.currency = currency
            instance.trial_period_days = trial_period_days
            instance.is_active = is_active
            instance.stripe_price_id = new_stripe_price_id
            instance.save()
            
            serializer = self.get_serializer(instance)
            return response.Response(serializer.data, status=200)
            
        except stripe.error.StripeError as e:
            return response.Response(
                {"error": f"Stripe error: {str(e)}"},
                status=400
            )
        except Exception as e:
            return response.Response(
                {"error": str(e)},
                status=400
            )
            
class PaymentPlanDeleteView(generics.DestroyAPIView):
    """
    API view to delete a payment plan.
    """
    queryset = PaymentPlan.objects.all()
    serializer_class = PaymentPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(
            {"message": "Payment plan deleted successfully"},
            status=status.HTTP_200_OK
        )
