from rest_framework import serializers
from triage.models import (
    Patient, 
    TriageRecord, 
    TriageResult, 
    VitalSigns, 
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
        fields = ['id', 'priority_level', 'treatment_area', 'triage_status', 'department', 'patient_nextstep']  

class VitalListSerializer(serializers.ModelSerializer):
    VALID_POSITIONS = ['L', 'B', 'C', 'A', 'H', 'P']  # Add all valid codes

    injury_position = serializers.ListField(
        child=serializers.CharField(max_length=1),  # Limit to single character
        required=False,
        allow_empty=True,
        allow_null=True
    )

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        
        if 'injury_position' in validated_data and validated_data['injury_position']:
            # Convert list to comma-separated string
            validated_data['injury_position'] = ','.join(validated_data['injury_position'])
        
        return validated_data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        
        if instance.injury_position:
            # Clean and process the string
            cleaned = instance.injury_position.replace("'", "").replace("[", "").replace("]", "")
            positions = [pos.strip() for pos in cleaned.split(',') if pos.strip()]
            ret['injury_position'] = positions
                
        return ret

    class Meta:
        model = VitalSigns
        fields = [
            'id',
            'injury_type',
            'injury_position'
        ]

class HistoryInfoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriageHistoryInfo
        fields = [
            'id',
            'guahao_status',
            'edit_triage',
            'departure_time',
            'stay_duration'
        ]

class TriageHistoryListSerializer(serializers.ModelSerializer):
    patient = PatientListSerializer(read_only=True)
    result = ResultListSerializer(read_only=True)
    vitalsigns = VitalListSerializer(read_only=True)
    history_info = HistoryInfoListSerializer(read_only=True)

    class Meta:
        model = TriageRecord
        fields = [
            'id',
            'registration_time', 
            'patient',
            'result',
            'vitalsigns',
            'history_info',
            'chief_complaint',
            'chief_symptom',
            'nurse',
            'speed_channel',
            'specialty_type'
        ]

