from payment.views.permission_views import HasActiveSubscription
from service.serializers.contact_cration_serilizers import ContactCreationFileSerializer, ContactCreationSerializer
from rest_framework import status, generics, permissions, response
from service.models import ContactCreationFile

class ContactCreationView(generics.CreateAPIView):
    serializer_class = ContactCreationSerializer
    permission_classes = [HasActiveSubscription]
    
    def post(self, request, *args, **kwargs):
        # Pass request in context so serializer can access request.user
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        
        contact_file = result.get("contact_file")

        return response.Response({
            "message": "Contact created successfully",
            "file_id": contact_file.id,
            "file_url": request.build_absolute_uri(contact_file.file.url),
            "title": contact_file.title,
            # "pdf_path": result.get("pdf_path")
        }, status=status.HTTP_201_CREATED)
        
        
class ContactCreationFileListView(generics.ListAPIView):
    serializer_class = ContactCreationFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter by current user
        return ContactCreationFile.objects.filter(user=self.request.user)