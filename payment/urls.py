from django.urls import path # type: ignore
from payment.views.payment_subscription_views import PaymentSubscriptionViews
from payment.views.payment_webhook_views import WebhookViews
from payment.views.pyment_plan_views import PaymentPlanDeleteView, PaymentPlanListView, PaymentPlanCreateView, PaymentPlanUpdateView

urlpatterns = [
    path('plans/', PaymentPlanListView.as_view(), name='payment-plan-list'),
    path('plans/create/', PaymentPlanCreateView.as_view(), name='payment-plan-create'),
    path('plans/update/<int:pk>/', PaymentPlanUpdateView.as_view(), name='payment-plan-update'),
    path('plans/delete/<int:pk>/', PaymentPlanDeleteView.as_view(), name='payment-plan-delete'),
    
    # Subscription URLs
    path('subscriptions/create/', PaymentSubscriptionViews.as_view(), name='payment-subscription-create'),
    path('webhook/', WebhookViews.as_view(), name='payment-webhook'),
]