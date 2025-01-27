from rest_framework import serializers
from ..models import MassInjury
from django.db.models import Count

class MassInjurySerializer(serializers.ModelSerializer):
    mass_triaged = serializers.IntegerField(read_only=True)  # Add calculated field
    mass_type_display = serializers.CharField(source='get_mass_type_display', read_only=True)  # Add display name
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)  # Add hospital name for display

    class Meta:
        model = MassInjury
        fields = [
            'id', 'mass_time', 'mass_type', 'mass_type_display',
            'mass_name', 'mass_number', 'mass_notes', 'mass_triaged', 'hospital_name'
        ]

# 新建群伤
class MassInjuryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MassInjury
        fields = [
            'mass_time',
            'mass_type',
            'mass_name',
            'mass_number',
            'mass_notes'
        ]

    def validate_mass_number(self, value):
        if value <= 0:
            raise serializers.ValidationError("群伤人数必须大于0")
        return value