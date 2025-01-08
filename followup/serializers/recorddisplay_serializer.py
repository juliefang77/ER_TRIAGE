from rest_framework import serializers
from triage.models import TriageRecord
from triage.serializers import PatientSerializer, MedicalStaffSerializer, TriageResultSerializer, HospitalUserFilterSerializer
from followup.models import FollowupRecipient

class FollowupRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowupRecipient
        fields = '__all__'

class FollowupTriageRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(required=False, allow_null=True)
    nurse = MedicalStaffSerializer(required=False, allow_null=True)
    hospital = HospitalUserFilterSerializer(required=False, allow_null=True)
    recipient = FollowupRecipientSerializer(required=False, allow_null=True)
    result = TriageResultSerializer(required=False, allow_null=True) 
    has_followup = serializers.BooleanField(read_only=True)

    class Meta:
        model = TriageRecord
        fields = [
            'id',
            'patient',
            'nurse',
            'hospital',
            'recipient',
            'result',
            'registration_time',  
            'chief_complaint',
            'chief_symptom',
            'medical_history',
            'surgery_type',
            'ifmass_injury',
            'has_followup'       # annotated field
        ]