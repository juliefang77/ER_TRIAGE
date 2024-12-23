from django_filters import rest_framework as filters
from .models import TriageRecord

class TriageRecordFilter(filters.FilterSet):
    # Filter by date range
    start_date = filters.DateTimeFilter(field_name='registration_time', lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name='registration_time', lookup_expr='lte')
    
    # Filter by triage result fields
    priority_level = filters.NumberFilter(field_name='result__priority_level')
    area = filters.CharFilter(field_name='result__area')
    
    # Filter by patient info
    patient_id = filters.CharFilter(field_name='patient__id_number')
    patient_name = filters.CharFilter(field_name='patient__name_chinese')

    class Meta:
        model = TriageRecord
        fields = [
            'start_date', 
            'end_date', 
            'priority_level',
            'area',
            'patient_id',
            'patient_name'
        ]