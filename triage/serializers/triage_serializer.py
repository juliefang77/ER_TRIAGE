from rest_framework import serializers
from django.contrib.auth import authenticate
from ..models import (
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

# For other serializers to use to filter for their own patients
class HospitalUserFilterSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(read_only=True)  
    
    class Meta:
        model = HospitalUser
        fields = ['id', 'hospital'] 

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
        fields = '__all__'


# Feed into 分诊记录 API
class TriageHistoryInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TriageHistoryInfo
        fields = '__all__'
        read_only_fields = ('stay_duration',)  # Only this is read-only because it's calculated

# 新建分诊 API serializer 
class TriageRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(required=False, allow_null=True, read_only=True)
    result = TriageResultSerializer(required=False, allow_null=True, read_only=True)
    vitalsigns = VitalSignsSerializer(required=False, allow_null=True, read_only=True)
    history_info = TriageHistoryInfoSerializer(required=False, allow_null=True, read_only=True)

    class Meta:
        model = TriageRecord
        fields = '__all__'

# 分诊记录API CRUD
class TriageHistorySerializer(serializers.ModelSerializer):
    patient = PatientSerializer(required=False, allow_null=True)
    result = TriageResultSerializer(required=False, allow_null=True)
    vitalsigns = VitalSignsSerializer(required=False, allow_null=True)
    history_info = TriageHistoryInfoSerializer(required=False, allow_null=True)

    class Meta:
        model = TriageRecord
        fields = '__all__'
    
    def update(self, instance, validated_data):
        # Handle nested updates
        patient_data = validated_data.pop('patient', None)
        result_data = validated_data.pop('result', None)
        vitalsigns_data = validated_data.pop('vitalsigns', None)
        history_info_data = validated_data.pop('history_info', None)

        # Update main instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update patient if data provided
        if patient_data and instance.patient:
            for attr, value in patient_data.items():
                setattr(instance.patient, attr, value)
            instance.patient.save()

        # Update result if data provided
        if result_data and instance.result:
            for attr, value in result_data.items():
                setattr(instance.result, attr, value)
            instance.result.save()

        # Update vitalsigns if data provided
        if vitalsigns_data and instance.vitalsigns:
            for attr, value in vitalsigns_data.items():
                setattr(instance.vitalsigns, attr, value)
            instance.vitalsigns.save()

        # Update history_info if data provided
        if history_info_data and instance.history_info:
            for attr, value in history_info_data.items():
                setattr(instance.history_info, attr, value)
            instance.history_info.save()

        return instance

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

