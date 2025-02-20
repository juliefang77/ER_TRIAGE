from django_filters import rest_framework as filters
from .models import TriageRecord, MassInjury

class TriageRecordFilter(filters.FilterSet):
    # Existing date range filters
    def filter_queryset(self, queryset):
        
        # Handle list values from QueryDict
        if 'start_date' in self.data:
            start_date = self.data.get('start_date')
            if isinstance(start_date, list):  # Check if it's a list
                start_date = start_date[0]    # Take first value
            self.data = dict(self.data)       # Make mutable copy
            self.data['start_date'] = start_date

        if 'end_date' in self.data:
            end_date = self.data.get('end_date')
            if isinstance(end_date, list):     # Check if it's a list
                end_date = end_date[0]         # Take first value
            self.data = dict(self.data)        # Make mutable copy
            self.data['end_date'] = end_date

        filtered = super().filter_queryset(queryset)
        return filtered

    start_date = filters.CharFilter(field_name='registration_time', lookup_expr='gte')
    end_date = filters.CharFilter(field_name='registration_time', lookup_expr='lte')

    # TriageResult filters
    priority_level = filters.NumberFilter(
        field_name='result__priority_level',
        lookup_expr='exact'  # Add this to ensure exact matching
    )

    triage_status = filters.CharFilter(field_name='result__triage_status')
    treatment_area = filters.CharFilter(field_name='result__treatment_area')
    department = filters.CharFilter(field_name='result__department')
    patient_nextstep = filters.CharFilter(field_name='result__patient_nextstep')
    triage_group = filters.NumberFilter(field_name='result__triage_group')

    # TriageRecord filters
    speed_channel = filters.CharFilter(field_name='speed_channel')
    specialty_type = filters.CharFilter(field_name='specialty_type')
    arrival_method = filters.CharFilter(field_name='arrival_method')
    ifmass_injury = filters.CharFilter(field_name='ifmass_injury')

    # Patient filters
    date_of_birth = filters.DateFilter(field_name='patient__date_of_birth')
    name_patient = filters.CharFilter(field_name='patient__name_patient', lookup_expr='icontains')

    # TriageHistoryInfo filters
    guahao_status = filters.CharFilter(field_name='history_info__guahao_status')

    class Meta:
        model = TriageRecord
        fields = [
            'start_date',
            'end_date',
            'priority_level',
            'triage_status',
            'treatment_area',
            'department',
            'patient_nextstep',
            'triage_group',
            'speed_channel',
            'specialty_type',
            'arrival_method',
            'ifmass_injury',
            'date_of_birth',
            'name_patient',
            'guahao_status'
        ]

    
