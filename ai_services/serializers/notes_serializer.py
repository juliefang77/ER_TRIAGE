from rest_framework import serializers
from followup.models import FollowupNotetaking

# Notes list 
class AiNotesListSerializer(serializers.ModelSerializer):
    name_patient = serializers.CharField(source='patient.name_patient')
    patient_phone = serializers.CharField(source='patient.patient_phone')

    class Meta:
        model = FollowupNotetaking
        fields = [
            'id',
            'name_patient',
            'patient_phone',
            'raw_notes',
            'processed_notes',
            'created_at'
        ]