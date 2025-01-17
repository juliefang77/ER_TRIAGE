from django_filters import rest_framework as filters
from triage.models import TriageRecord, TriageResult
from followup.models import FollowupRecipient

class FollowupMainFilter(filters.FilterSet):
    # Date range filters
    start_date = filters.CharFilter(field_name='registration_time', lookup_expr='gte')
    end_date = filters.CharFilter(field_name='registration_time', lookup_expr='lte')
    
    # TriageResult filters
    priority_level = filters.ChoiceFilter(  # Changed to ChoiceFilter
        field_name='result__priority_level',
        choices=TriageResult.PRIORITY_LEVELS
    )

    # TriageRecord filters
    specialty_type = filters.ChoiceFilter(  # Changed to ChoiceFilter
        field_name='specialty_type',
        choices=TriageRecord.SPECIALTY_TYPE_CHOICES
    )

    # Patient filters
    date_of_birth = filters.DateFilter(field_name='patient__date_of_birth')
    name_patient = filters.CharFilter(field_name='patient__name_patient', lookup_expr='icontains')

    #TriageRecipient filters
    message_reply = filters.ChoiceFilter(
        field_name='recipient__message_reply',
        choices=FollowupRecipient.MESSAGE_REPLY_CHOICES
    )
    
    survey_status = filters.ChoiceFilter(
        field_name='recipient__survey_status',
        choices=FollowupRecipient.SURVEY_STATUS_CHOICES
    )
    
    call_status = filters.ChoiceFilter(
        field_name='recipient__call_status',
        choices=FollowupRecipient.CALL_STATUS_CHOICES
    )

    class Meta:
        model = TriageRecord  # Changed to TriageRecord since that's our main model
        fields = [
            'start_date', 
            'end_date', 
            'priority_level',
            'specialty_type',
            'name_patient',
            'date_of_birth',
            'message_reply',
            'survey_status',
            'call_status'
        ]

class AiSurveyRecipientFilter(filters.FilterSet):
    # Date range filters for registration time
    start_date = filters.CharFilter(field_name='triage_record__registration_time', lookup_expr='gte')
    end_date = filters.CharFilter(field_name='triage_record__registration_time', lookup_expr='lte')
    
    # Specialty type filter
    specialty_type = filters.CharFilter(field_name='triage_record__specialty_type')
    
    # Priority level filter
    priority_level = filters.CharFilter(field_name='triage_record__result__priority_level')

    class Meta:
        model = FollowupRecipient
        fields = ['start_date', 'end_date', 'specialty_type', 'priority_level']