from rest_framework import serializers
from followup.models import BookingOnline

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingOnline
        fields = ['hospital', 'start_time', 'end_time']  # Fields that patient can set
        read_only_fields = ['status', 'patient_user', 'terminal_trace', 'payment_id']  # Fields set by system

class BookingDetailSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient_user.first_name', read_only=True)
    patient_phone = serializers.CharField(source='patient_user.phone', read_only=True)
    
    class Meta:
        model = BookingOnline
        fields = '__all__'