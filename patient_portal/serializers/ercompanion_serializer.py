from rest_framework import serializers
from ..models import ErCompanion

class ErCompanionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErCompanion
        fields = [
            'id',
            'priority_response',
            'symptom_response',
            'medication_response',
            'heart_level',
            'energy_level',
            'waiting_feel',
            'complete_step1',
            'complete_step2',
            'complete_step3'
        ]