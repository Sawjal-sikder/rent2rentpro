from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.permissions import IsAdminUser  # type: ignore
from dashboard.serializers.dashboard_serializer import DashboardSerializer  # type: ignore
from django.contrib.auth import get_user_model # type: ignore
User = get_user_model()

from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncMonth

class DashboardView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        serializer = DashboardSerializer(instance={})
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        


class UserInsightsView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        # Get the current date
        current_date = timezone.now()

        # Get the date for 12 months ago
        twelve_months_ago = current_date - timedelta(days=365)

        # Query for user registrations by type, grouped by month
        user_insights = User.objects.filter(
            created_at__gte=twelve_months_ago
        ).annotate(month=TruncMonth('created_at')) \
          .values('month', 'user_type') \
          .annotate(count=Count('id')) \
          .order_by('month', 'user_type')

        # Prepare the result dictionary
        insights_data = {}

        for i in range(12):
            month = (current_date - timedelta(days=30*i)).replace(day=1)  # First day of each month
            # Format as "Jan-26"
            month_str = month.strftime('%b-%y')  # '%b' = Month abbreviation (Jan, Feb, etc.), '%y' = last 2 digits of year
            insights_data[month_str] = {
                'individuals': 0,
                'company': 0
            }

        # Populate insights_data with the actual counts
        for insight in user_insights:
            month_str = insight['month'].strftime('%b-%y')  # Format as "Jan-26"
            user_type = insight['user_type']
            insights_data[month_str][user_type] = insight['count']

        return Response({
            "success": True,
            "user_insights": insights_data
        }, status=status.HTTP_200_OK)