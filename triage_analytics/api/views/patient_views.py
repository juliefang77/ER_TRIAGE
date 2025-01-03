from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # Add this import
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from triage.models import HospitalUser, Hospital, TriageRecord

from ..serializers.patient_serializers import DateRangeSerializer, DistributionResponseSerializer
from ...services.stats.patient_stats import PatientDistributionStats

class PatientStatsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]  

    def get_queryset(self):
        # Get base queryset filtered by hospital
        return TriageRecord.objects.filter(
            hospital=self.request.user.hospital
        )
    
    def _get_validated_dates(self, request):
        """Helper method to validate date parameters"""
        date_serializer = DateRangeSerializer(data=request.query_params)
        date_serializer.is_valid(raise_exception=True)
        return date_serializer.validated_data

    @action(detail=False, methods=['GET'])
    def priority_distribution(self, request):
        """
        获取急诊患者分级分布
        GET /apichart/patientstats/priority_distribution/
        """
        user: HospitalUser = request.user  # Type hint for user

        if not request.user.hospital:
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
        """
        获取急诊患者科室分布
        GET /api/triage-analytics/patient-stats/department-distribution/
        """
        if not request.user.hospital:
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
        if not request.user.hospital:
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