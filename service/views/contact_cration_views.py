from payment.views.permission_views import HasActiveSubscription
from service.serializers.contact_cration_serilizers import ContactCreationSerializer  # type: ignore
from rest_framework import status, generics, permissions, response  # type: ignore

class ContactCreationView(generics.CreateAPIView):
    serializer_class = ContactCreationSerializer
    permission_classes = [HasActiveSubscription]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        return response.Response({
            "message": "Contact created successfully",
            "data": serializer.validated_data,
            "pdf_url": request.build_absolute_uri("/") + result["pdf_path"]
        }, status=status.HTTP_201_CREATED)
