from django_filters import rest_framework as filters
from .models import TriageRecord

class TriageRecordFilter(filters.FilterSet):
    # Existing date range filters
    start_date = filters.DateTimeFilter(field_name='registration_time', lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name='registration_time', lookup_expr='lte')

    # TriageResult filters
    priority_level = filters.NumberFilter(field_name='result__priority_level')
    triage_status = filters.CharFilter(field_name='result__status')
    treatment_area = filters.CharFilter(field_name='result__area')
    department = filters.CharFilter(field_name='result__department')
    patient_nextstep = filters.CharFilter(field_name='result__next_step')
    triage_group = filters.NumberFilter(field_name='result__group')

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