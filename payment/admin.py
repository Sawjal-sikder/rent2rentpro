from django.contrib import admin #type: ignore
from .models import PaymentPlan, Subscription



@admin.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'interval', 'currency', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'stripe_product_id', 'stripe_price_id')
    list_filter = ('is_active', 'interval', 'currency')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_plan', 'status', 'start_date', 'end_date', 'is_active', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'payment_plan__name', 'stripe_customer_id', 'stripe_subscription_id')
    list_filter = ('status', 'is_active')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')