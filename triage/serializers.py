from rest_framework import serializers
from .models import Patient, TriageRecord, VitalSigns, MedicalStaff

class MedicalStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalStaff
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class TriageRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    nurse = MedicalStaffSerializer(read_only=True)  # Add this too
    
    class Meta:
        model = TriageRecord
        fields = '__all__'

class VitalSignsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSigns
        fields = '__all__'