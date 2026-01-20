from rest_framework import serializers #type: ignore
from payment.models import Subscription

class PaymentSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['id', 'stripe_customer_id', 'stripe_subscription_id', 'status', 'start_date', 'end_date', 'created_at', 'updated_at']