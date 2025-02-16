from rest_framework import serializers
from patient_portal.models import PatientFeedback

class PatientFeedbackSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient_user.first_name', read_only=True)
    
    class Meta:
        model = PatientFeedback
        fields = [
            'id',
            'patient_name',
            'contact_phone',
            'request_type',
            'request_content',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'patient_name']