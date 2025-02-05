from rest_framework import serializers
from followup.models import BookingOnline

# 患者下订单
class BookingCreateSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)  # Add hospital name
    
    class Meta:
        model = BookingOnline
        fields = [
            'id', 'hospital', 'hospital_name',  # Add hospital name for reading
            'date_of_birth', 'old_patient', 'complaint',
            'start_time', 'end_time',
            'status'  # Add status for reading
        ]
        read_only_fields = [
            'status', 'patient_user', 'terminal_trace', 'payment_id', 'hospital_name'
        ]  # These can't be set by patient

class BookingDetailSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient_user.first_name', read_only=True)
    patient_phone = serializers.CharField(source='patient_user.phone', read_only=True)
    
    class Meta:
        model = BookingOnline
        fields = '__all__'

# 医院看订单 list
class HospitalBookingSerializer(serializers.ModelSerializer):
    # Add nested patient user fields
    patient_name = serializers.CharField(source='patient_user.first_name', read_only=True)
    patient_phone = serializers.CharField(source='patient_user.phone', read_only=True)

    class Meta:
        model = BookingOnline
        fields = [
            'id', 'hospital', 'start_time', 'end_time', 'status', 'actual_time',
            'old_patient', 'complaint', 'date_of_birth', 'reject_reason',
            'patient_name', 'patient_phone',  # Add the new fields
            'terminal_trace', 'payment_id'
        ]
        read_only_fields = ['patient_user', 'terminal_trace', 'payment_id']