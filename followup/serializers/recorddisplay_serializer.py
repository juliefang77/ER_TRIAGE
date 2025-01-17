from rest_framework import serializers
from triage.models import TriageRecord, VitalSigns, Patient, TriageResult
from triage.serializers.triage_serializer import HospitalUserFilterSerializer
from followup.models import FollowupRecipient

class FollowupRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowupRecipient
        fields = '__all__'

class InjurySerializer(serializers.ModelSerializer):
    injury_position = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
        allow_null=True
    )

    class Meta:
        model = VitalSigns
        fields = [
            'id',
            'injury_type',
            'injury_position'
        ]

class SimplePatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id_system', 'name_patient', 'patient_phone', 'gender', 'date_of_birth', 'age']  

class SimpleResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriageResult
        fields = ['id', 'priority_level', 'department']


class FollowupTriageRecordSerializer(serializers.ModelSerializer):
    patient = SimplePatientSerializer(required=False, allow_null=True)
    # nurse = MedicalStaffSerializer(required=False, allow_null=True)
    hospital = HospitalUserFilterSerializer(required=False, allow_null=True)
    recipient = FollowupRecipientSerializer(required=False, allow_null=True)
    result = SimpleResultSerializer(required=False, allow_null=True) 
    vitalsigns = InjurySerializer(required=False, allow_null=True)
    has_followup = serializers.BooleanField(read_only=True)
    has_note = serializers.BooleanField(read_only=True)  # Add new field

    class Meta:
        model = TriageRecord
        fields = [
            'id',
            'patient',
            'nurse',
            'hospital',
            'recipient',
            'result',
            'vitalsigns',
            'registration_time',  
            'chief_complaint',
            'chief_symptom',
            'specialty_type',
            'has_followup',       # annotated field
            'has_note'       # annotated field
        ]