import os
from rest_framework import serializers
from service.models import ContactCreationFile
from service.utils.contact_creation_generate_pdf import generate_pdf
from django.core.files.base import ContentFile

class ContactCreationSerializer(serializers.Serializer):
    contact_type = serializers.ChoiceField(choices=[
        ('Ingenieurswohnung', 'Ingenieurswohnung'),
        ('Monteurswohnung', 'Monteurswohnung'),
        ('WG-Zimmer', 'WG-Zimmer'),
        ('Senioren-WG', 'Senioren-WG')
    ])
    landlord_name = serializers.CharField(max_length=100)
    landlord_address = serializers.CharField(max_length=255)
    landlord_email = serializers.EmailField()
    tenant_name = serializers.CharField(max_length=100)
    tenant_address = serializers.CharField(max_length=255)
    tenant_email = serializers.EmailField()
    property_address = serializers.CharField(max_length=255)
    property_appartment_number = serializers.CharField(max_length=50, required=False, allow_blank=True)
    property_room_count = serializers.IntegerField()
    property_is_furnished = serializers.BooleanField()
    rent_type = serializers.ChoiceField(choices=['flat rate', 'plus utilities'])
    rent_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    rent_contact_start_date = serializers.DateField()
    rent_contact_end_date = serializers.DateField(required=False, allow_null=True)
    rent_reason_contract_limitations = serializers.CharField(max_length=255, required=False, allow_blank=True)
    rent_term_monthly_rent = serializers.DecimalField(max_digits=10, decimal_places=2)
    rent_security_deposit = serializers.DecimalField(max_digits=10, decimal_places=2)
    rent_contract_duration_months = serializers.IntegerField()
    rent_start_date = serializers.DateField()
    contract_limitation_reason = serializers.CharField(max_length=255, required=False, allow_blank=True)
    contract_limitation_details = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def create(self, validated_data):
        # Get user from context
        user = self.context['request'].user
        
        # Generate the PDF file
        pdf_path = generate_pdf(validated_data)
        
        # Create a title for the contract
        title = f"{validated_data['contact_type']}_Contract_{validated_data['tenant_name']}_{validated_data['rent_start_date']}"
        
        # Read the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
        
        # Create ContactCreationFile instance with user
        contact_file = ContactCreationFile.objects.create(
            user=user,  # Add the user here
            title=title,
            file=ContentFile(pdf_content, name=os.path.basename(pdf_path))
        )
        
        # Add both pdf_path and contact_file to validated_data
        validated_data["contact_file"] = contact_file
        validated_data["pdf_path"] = pdf_path
        
        return validated_data


class ContactCreationFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactCreationFile
        fields = ['id', 'title', 'file', 'created_at', 'updated_at']