from rest_framework import generics, permissions # type: ignore
from dashboard.serializers.tenant_management_serializer import ContactCreationFileSerializer
from service.models import ContactCreationFile # type: ignore
from dashboard.views.pagination_views import SetPagination # type: ignore


class TenantManagementView(generics.ListAPIView):
    queryset = ContactCreationFile.objects.all()
    serializer_class = ContactCreationFileSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = SetPagination