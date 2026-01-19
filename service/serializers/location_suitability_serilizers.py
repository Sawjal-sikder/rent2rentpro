from rest_framework import serializers
from service.models import LocationSuitability
from service.utils.agent_request import generate_location_request
import os
from django.urls import reverse

class LocationSuitabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationSuitability
        fields = [
            'id',
            'user',
            'city_size',
            'district_type',
            'demand_profile',
            'public_transport',
            'supermarkets_restaurants',
            'universities_hospitals_offices',
            'local_demand',
            'competition_level',
            'short_term_prices',
            'regulatory_friendliness',
            'analysis_summary',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'analysis_summary']
        
    def validate(self, attrs):
        city_size = attrs.get('city_size')
        district_type = attrs.get('district_type')
        demand_profile = attrs.get('demand_profile')
        public_transport = attrs.get('public_transport')
        supermarkets_restaurants = attrs.get('supermarkets_restaurants')
        universities_hospitals_offices = attrs.get('universities_hospitals_offices')
        local_demand = attrs.get('local_demand')
        competition_level = attrs.get('competition_level')
        short_term_prices = attrs.get('short_term_prices')
        regulatory_friendliness = attrs.get('regulatory_friendliness')
        
        if not all([city_size, district_type, demand_profile, public_transport,
                    supermarkets_restaurants, universities_hospitals_offices,
                    local_demand, competition_level, short_term_prices,
                    regulatory_friendliness]):
            raise serializers.ValidationError("All fields must be provided and non-empty.")
        return attrs
    
    def create(self, validated_data):
        # Get the request object from context
        request = self.context.get('request')
        
        analysis_summary = {}
        validated_data['analysis_summary'] = analysis_summary
        location_suitability = LocationSuitability.objects.create(**validated_data)
        
        # Start the async task
        task = generate_location_request.delay(
            os.getenv("BASE_URL_AI_SERVICE") + "/ai/location_analysis",
            payload={
                "city_size": validated_data['city_size'],
                "district_type": validated_data['district_type'],
                "demand_profile": validated_data['demand_profile'],
                "public_transport": validated_data['public_transport'],
                "supermarkets_restaurants": validated_data['supermarkets_restaurants'],
                "universities_hospitals_offices": validated_data['universities_hospitals_offices'],
                "local_demand": validated_data['local_demand'],
                "competition_level": validated_data['competition_level'],
                "short_term_prices": validated_data['short_term_prices'],
                "regulatory_friendliness": validated_data['regulatory_friendliness'],
            },
            location_suitability_id=location_suitability.id 
        )
        
        # Store task_id for tracking (optional, if you have a field for it)
        # location_suitability.task_id = task.id
        # location_suitability.save()
        
        # Build the detail URL
        detail_url = request.build_absolute_uri(
            reverse('location-suitability-detail', kwargs={'pk': location_suitability.id})
        )
        
        # Prepare the response data
        response_data = {
            'id': location_suitability.id,
            'task_id': task.id,
            'status': 'processing',
            'redirect_url': detail_url,
            'analysis_summary': analysis_summary,
            # Add other fields from location_suitability as needed
        }
        
        return response_data

    def update(self, instance, validated_data):
        update_location_suitability = super().update(instance, validated_data)
        return update_location_suitability