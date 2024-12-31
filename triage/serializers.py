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

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'address', 'contact_number', 'is_active']

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

class TriageRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    nurse = MedicalStaffSerializer()
    result = TriageResultSerializer() 
    vital_signs = VitalSignsSerializer()

    class Meta:
        model = TriageRecord
        fields = '__all__'

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