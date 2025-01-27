from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from triage.models import TriageRecord, VitalSigns, TriageResult, MedicalStaff
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from ..filters import TriageRecordFilter
from triage.serializers.triage_serializer import (
    TriageHistorySerializer, 
    TriageResultSerializer, 
    VitalSignsSerializer, 
    MedicalStaffSerializer)
from triage.serializers.history_serializer import TriageHistoryListSerializer

# Custom pagination class
class TriageHistoryPagination(PageNumberPagination):
    page_size = 20  # Number of records per page
    page_size_query_param = 'page_size'
    max_page_size = 100

# 分诊记录，含所有细节 (CRUD)
class TriageHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = TriageHistorySerializer  # Full serializer
    pagination_class = TriageHistoryPagination

    def get_queryset(self):
        return TriageRecord.objects.select_related(
            'patient',
            'result',
            'vitalsigns',
            'history_info'
        ).filter(hospital=self.request.user.hospital)  # Keep only the security filter
        

class SaaSMedicalStaffViewSet(viewsets.ModelViewSet):
    queryset = MedicalStaff.objects.all()
    serializer_class = MedicalStaffSerializer

# 分诊记录list view
class TriageHistoryListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TriageHistoryListSerializer
    pagination_class = TriageHistoryPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter
    ]
    filterset_class = TriageRecordFilter
    ordering = ['-registration_time']

    def get_queryset(self):
        return TriageRecord.objects.select_related(
            'patient',
            'result',
            'vitalsigns',
            'history_info'
        ).only(
            # TriageRecord fields
            'id',
            'registration_time',
            'chief_complaint',
            'chief_symptom',
            # Patient fields
            'patient__id_system',
            'patient__name_patient',
            'patient__gender',
            'patient__id_type',
            'patient__id_number',
            'patient__date_of_birth',
            # Result fields
            'result__id',
            'result__priority_level',
            'result__treatment_area',
            'result__triage_status',
            # VitalSigns fields
            'vitalsigns__id',
            'vitalsigns__injury_type',
            'vitalsigns__injury_position',
            # HistoryInfo fields
            'history_info__id',
            'history_info__guahao_status',
            'history_info__departure_time',
            'history_info__stay_duration'
        ).filter(hospital=self.request.user.hospital)