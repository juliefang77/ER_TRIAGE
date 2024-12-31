from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    Patient, 
    TriageRecord, 
    TriageResult, 
    VitalSigns, 
    MedicalStaff, 
    Hospital, 
    HospitalUser, 
    TriageHistoryInfo
)
# Change patient form status to APPROVED upon approval
from patient_portal.models import PatientTriageSubmission

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

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
    # Add custom field handling for multiple injury positions
    injury_position = serializers.MultipleChoiceField(
        choices=VitalSigns.INJURY_POSITIONS,  # Access through the model
        required=False
    )

    class Meta:
        model = VitalSigns
        fields = '__all__'

    def to_representation(self, instance):
        # Convert comma-separated string to list when reading
        ret = super().to_representation(instance)
        if ret['injury_position']:
            ret['injury_position'] = ret['injury_position'].split(',')
        return ret

    def to_internal_value(self, data):
        # Convert list back to comma-separated string when writing
        if 'injury_position' in data and isinstance(data['injury_position'], list):
            data['injury_position'] = ','.join(data['injury_position'])
        return super().to_internal_value(data)

class TriageHistoryInfoSerializer(serializers.ModelSerializer):
    # All fields editable except stay_duration
    assigned_doctor = MedicalStaffSerializer()
    assigned_nurse = MedicalStaffSerializer()

    class Meta:
        model = TriageHistoryInfo
        fields = '__all__'
        read_only_fields = ('stay_duration',)  # Only this is read-only because it's calculated

# 新建分诊 API serializer 
class TriageRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(required=False)
    vital_signs = VitalSignsSerializer(required=False)
    result = TriageResultSerializer(required=False)
    nurse = MedicalStaffSerializer(required=False)

    class Meta:
        model = TriageRecord
        fields = '__all__'

    def create(self, validated_data):
        # Pop nested data
        patient_data = validated_data.pop('patient', None)
        vital_signs_data = validated_data.pop('vital_signs', None)
        result_data = validated_data.pop('result', None)
        nurse_data = validated_data.pop('nurse', None)
        submission_id = validated_data.pop('submission_id', None)

        # Create the triage record first
        triage_record = TriageRecord.objects.create(**validated_data)

        # Create or update related objects if data exists
        if patient_data:
            patient, _ = Patient.objects.get_or_create(
                id_number=patient_data.get('id_number'),
                defaults=patient_data
            )
            triage_record.patient = patient

        if vital_signs_data:
            vital_signs = VitalSigns.objects.create(
                triage_record=triage_record,
                **vital_signs_data
            )

        if result_data:
            result = TriageResult.objects.create(
                triage_record=triage_record,
                **result_data
            )

        if nurse_data:
            nurse, _ = MedicalStaff.objects.get_or_create(**nurse_data)
            triage_record.nurse = nurse

        # Update submission status if submission_id exists
        if submission_id:
            PatientTriageSubmission.objects.filter(
                id=PatientTriageSubmission.submission_id,
                hospital=validated_data.get('hospital')  # Get hospital from validated_data
            ).update(status='APPROVED')

        triage_record.save()
        return triage_record

# For the history view that needs combined data (not used now)
class TriageHistorySerializer(serializers.ModelSerializer):
    # Remove read_only=True from all except calculated fields
    patient = PatientSerializer()
    nurse = MedicalStaffSerializer()
    result = TriageResultSerializer()
    vital_signs = VitalSignsSerializer()
    history_info = TriageHistoryInfoSerializer()

    class Meta:
        model = TriageRecord
        fields = '__all__'

#Authentication Serializers
class HospitalLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                              username=username, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class HospitalUserSerializer(serializers.ModelSerializer):
    """
    Note: This serializer is for admin management only, 
    not for hospital client authentication
    """
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = HospitalUser
        fields = ('id', 'username', 'password', 'email', 'first_name',
                 'last_name', 'hospital')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Force is_staff to False for all hospital users
        validated_data['is_staff'] = False
        user = HospitalUser.objects.create_user(**validated_data)
        return user