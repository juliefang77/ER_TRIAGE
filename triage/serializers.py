from rest_framework import serializers
from .models import Patient, TriageRecord, TriageResult, VitalSigns, MedicalStaff

class MedicalStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalStaff
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class TriageResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriageResult
        fields = '__all__'

class VitalSignsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSigns
        fields = '__all__'

class TriageRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    nurse = MedicalStaffSerializer(read_only=True)
    result = TriageResultSerializer(read_only=True)  # Add this to include triage result
    vital_signs = VitalSignsSerializer(read_only=True)

    class Meta:
        model = TriageRecord
        fields = '__all__'

# For the history view that needs combined data
class TriageHistorySerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    nurse = MedicalStaffSerializer(read_only=True)
    result = TriageResultSerializer(read_only=True)
    vital_signs = VitalSignsSerializer(read_only=True)

    class Meta:
        model = TriageRecord
        fields = '__all__'