from rest_framework import serializers #type: ignore
from payment.models import PaymentPlan

class PaymentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlan
        fields = [
            'id',
            'name',
            'stripe_product_id',
            'stripe_price_id',
            'amount',
            'interval',
            'currency',
            'trial_period_days',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']