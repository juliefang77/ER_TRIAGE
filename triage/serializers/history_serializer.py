from rest_framework import serializers
from triage.models import (
    Patient, 
    TriageRecord, 
    TriageResult, 
    VitalSigns, 
    MedicalStaff, 
    Hospital, 
    HospitalUser, 
    TriageHistoryInfo
)

class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id_system', 'name_patient', 'gender', 'id_type', 'id_number', 'date_of_birth']

class ResultListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriageResult
        fields = ['id', 'priority_level', 'treatment_area', 'triage_status']  

class VitalListSerializer(serializers.ModelSerializer):
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

class TriageHistoryListSerializer(serializers.ModelSerializer):
    patient = PatientListSerializer(read_only=True)
    result = ResultListSerializer(read_only=True)
    vitalsigns = VitalListSerializer(read_only=True)

    class Meta:
        model = TriageRecord
        fields = [
            'id',
            'registration_time', 
            'patient',
            'result',
            'vitalsigns',
            'chief_complaint',
            'chief_symptom'
        ]

