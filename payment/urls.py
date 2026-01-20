from django.urls import path # type: ignore
from payment.views.payment_subscription_views import PaymentSubscriptionViews
from payment.views.pyment_plan_views import PaymentPlanListView, PaymentPlanCreateView, PaymentPlanUpdateView

urlpatterns = [
    path('plans/', PaymentPlanListView.as_view(), name='payment-plan-list'),
    path('plans/create/', PaymentPlanCreateView.as_view(), name='payment-plan-create'),
    path('plans/update/<int:pk>/', PaymentPlanUpdateView.as_view(), name='payment-plan-update'),
    
    # Subscription URLs
    path('subscriptions/create/', PaymentSubscriptionViews.as_view(), name='payment-subscription-create'),
]