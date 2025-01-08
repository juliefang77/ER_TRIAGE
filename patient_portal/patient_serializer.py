# patient_portal/patient_serializer.py

from rest_framework import serializers
from .models import PatientTriageSubmission

# Patient filling form 
class PatientTriageSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientTriageSubmission
        fields = '__all__'


# Nurse views all PENDING patients as a list, read only
class PendingSubmissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientTriageSubmission
        fields = '__all__'


# Nurse opens an individual patient's page, and sees autofilling, can edit
class PendingSubmissionMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientTriageSubmission
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Handle injury_position as multiple choice
        injury_position = data['injury_position']
        if injury_position:
            # If it's stored as comma-separated string, convert to list
            if isinstance(injury_position, str):
                injury_position = injury_position.split(',')
            # If it's already a list, use as is
            elif not isinstance(injury_position, list):
                injury_position = [injury_position]
        
        mapped_data = {
            'patient_data': {
                'name_patient': data['name_patient'],
                'id_type': data['id_type'],
                'id_number': data['id_number'],
                'gender': data['gender'],
                'date_of_birth': data['date_of_birth'],
                'patient_phone': data['patient_phone'],
                'id_medical_insurance': data['id_medical_insurance'],
                'id_hospital_card': data['id_hospital_card'],
                'insurance_type': data['insurance_type'],
                'patient_type': data['patient_type'],
            },
            'vital_signs_data': {
                'temperature': data['temperature'],
                'pain_score': data['pain_score'],
                'injury_position': injury_position,  # Now handles multiple values
                'injury_type': data['injury_type'],
            },
            'triage_data': {
                'chief_complaint': data['chief_complaint'],
                'chief_symptom': data['chief_symptom'],
                'other_inquiry': data['other_inquiry'],
                'hospital': data['hospital'],
            }
        }
        
        return mapped_data

# Authentication
class PatientLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()

class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()