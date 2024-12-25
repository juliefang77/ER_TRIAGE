from rest_framework import serializers
from triage.models import Patient, TriageRecord, VitalSigns

class VitalSignsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSigns
        fields = ['temperature', 'pain_score']

class TriageRecordSerializer(serializers.ModelSerializer):
    vital_signs = VitalSignsSerializer()
    
    class Meta:
        model = TriageRecord
        fields = ['chief_complaint', 'vital_signs']

class PatientSelfRegistrationSerializer(serializers.ModelSerializer):
    triage_info = TriageRecordSerializer(write_only=True)  # For POST requests
    triage_records = TriageRecordSerializer(many=True, read_only=True)  # For GET requests

    class Meta:
        model = Patient
        fields = [
            'name_chinese',
            'id_type',
            'id_number',
            'triage_info',  # For creating
            'triage_records'  # For viewing
        ]

    def create(self, validated_data):
        triage_info = validated_data.pop('triage_info')
        vital_signs_data = triage_info.pop('vital_signs')

        # Create patient
        patient = Patient.objects.create(**validated_data)

        # Create triage record
        triage_record = TriageRecord.objects.create(
            patient=patient,
            **triage_info
        )

        # Create vital signs
        VitalSigns.objects.create(
            triage_record=triage_record,
            **vital_signs_data
        )

        return patient