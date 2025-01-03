from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # Add this import
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from triage.models import HospitalUser, Hospital, TriageRecord, TriageResult
from django.db.models import Count  # Add this import at the top

from ..serializers.patient_serializers import DateRangeSerializer, DistributionResponseSerializer
from ...services.stats.patient_stats import PatientDistributionStats

class PatientStatsViewSet(ReadOnlyModelViewSet):  # Change to ReadOnlyModelViewSet
    serializer_class = DateRangeSerializer  # Add a serializer class
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Explicitly start with TriageRecord
        return TriageRecord.objects.filter(
            hospital=self.request.user
        ).select_related('result')  # Add this to optimize the query
    
    def _get_validated_dates(self, request):
        """Helper method to validate date parameters"""
        date_serializer = DateRangeSerializer(data=request.query_params)
        date_serializer.is_valid(raise_exception=True)
        return date_serializer.validated_data

    @action(detail=False, methods=['GET'])
    def priority_distribution(self, request):
        if not isinstance(request.user, HospitalUser):  # Better type check
            raise ValidationError("用户未关联医院")
            
        dates = self._get_validated_dates(request)
        
        stats = PatientDistributionStats(
            queryset=self.get_queryset(),  # Use the queryset method
            start_date=dates['start_date'],
            end_date=dates['end_date']
        )
        
        distribution = stats.get_priority_level_distribution()
        response_serializer = DistributionResponseSerializer(data=distribution)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data)

    @action(detail=False, methods=['GET'])
    def department_distribution(self, request):
        if not isinstance(request.user, HospitalUser):  # Better type check
            raise ValidationError("用户未关联医院")
            
        dates = self._get_validated_dates(request)
        
        stats = PatientDistributionStats(
            queryset=self.get_queryset(),  # Use the queryset method
            start_date=dates['start_date'],
            end_date=dates['end_date']
        )
        
        distribution = stats.get_department_distribution()
        response_serializer = DistributionResponseSerializer(data=distribution)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data)

    @action(detail=False, methods=['GET'])
    def all_distributions(self, request):
        # 获取所有分布统计
        # GET /api/triage-analytics/patient-stats/all-distributions/
        if not isinstance(request.user, HospitalUser):  # Better type check
            raise ValidationError("用户未关联医院")
            
        dates = self._get_validated_dates(request)
        
        stats = PatientDistributionStats(
            queryset=self.get_queryset(),  # Use the queryset method
            start_date=dates['start_date'],
            end_date=dates['end_date']
        )
        
        return Response({
            'priority_level': stats.get_priority_level_distribution(),
            'department': stats.get_department_distribution()
        })