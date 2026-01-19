from rest_framework import generics, permissions, response, status # type: ignore
from service.models import LocationSuitability
from service.serializers.location_suitability_serilizers import LocationSuitabilitySerializer

class LocationSuitabilityView(generics.ListCreateAPIView):
    queryset = LocationSuitability.objects.all()
    serializer_class = LocationSuitabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save(user=self.request.user)
        return response.Response(response_data, status=status.HTTP_201_CREATED)
    
class LocationSuitabilityDetailView(generics.RetrieveAPIView):
    queryset = LocationSuitability.objects.all()
    serializer_class = LocationSuitabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)