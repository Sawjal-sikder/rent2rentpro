from django.db import models #type: ignore
from django.utils import timezone #type: ignore
from django.contrib.auth import get_user_model #type: ignore
User = get_user_model()

class PaymentPlan(models.Model):
    name = models.CharField(max_length=100)
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interval = models.CharField(max_length=150)
    currency = models.CharField(max_length=10, default='usd')
    trial_period_days = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        return self.name
    
class Subscription(models.Model):
    CHOICES_STATUS = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('pending', 'Pending'),
        ('trialing', 'Trialing'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_plan = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    
    status = models.CharField(max_length=50, choices=CHOICES_STATUS, default='pending')
    trial_start = models.DateTimeField(blank=True, null=True)
    trial_end = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    
    auto_renew = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        return f"{self.user.full_name} - {self.payment_plan.name}"
    

    @property
    def is_valid(self):
        """Check if subscription is currently valid"""
        return self.status in ['active', 'trialing'] and self.end_date and self.end_date > timezone.now()