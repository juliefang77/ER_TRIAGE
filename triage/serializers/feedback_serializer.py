from rest_framework import serializers
from triage.models import HospitalFeedback

class HospitalFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalFeedback
        fields = [
            'contact',
            'contact_phone',
            'request_type',
            'request_content',
            'created_at'
        ]
        read_only_fields = ['created_at']

