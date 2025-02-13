from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..services.baidu_survey import SurveyAnalysisService
from followup.models import FollowupRecipient, FollowupSurvey, SurveyAi
# Serializers
from ..serializers.survey_serializer import SurveyAnalysisListSerializer, SurveyAiSerializer, SurveyLLMAnalysisSerializer
from followup.serializers.survey_serializer import ManagementSurveyDetailSerializer
# Filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters


class SurveyAnalysisListViewSet(viewsets.ModelViewSet):
    serializer_class = SurveyAiSerializer
    
    def get_queryset(self):
        # Filter queryset to only show analyses for the current hospital
        return SurveyAi.objects.filter(
            hospital=self.request.user.hospital
        ).prefetch_related(
            'recipients'  # Add this to optimize the query
        ).order_by('-created_at')

# 分析问卷选择患者时的pagination
class SurveyAnalysisPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

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

class SurveyAnalysisViewSet(viewsets.ViewSet):
    filter_backends = [DjangoFilterBackend]
    pagination_class = SurveyAnalysisPagination
    filterset_class = AiSurveyRecipientFilter

    def list(self, request):
        # Get completed surveys with related data
        completed_recipients = FollowupRecipient.objects.filter(
            survey_status='YES_RESPONSE',
            hospital=request.user.hospital
        ).select_related(
            'triage_record',
            'triage_record__result',
            'patient',
        ).annotate(
            # Add any computed fields if needed
        )

        # Apply filters
        filtered_recipients = self.filterset_class(
            request.GET,
            queryset=completed_recipients
        ).qs

        # Add pagination
        paginator = self.pagination_class()
        paginated_recipients = paginator.paginate_queryset(filtered_recipients, request)
        
        serializer = SurveyAnalysisListSerializer(paginated_recipients, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def survey_detail(self, request, pk=None):
        # Get the specific recipient's survey details
        recipient = get_object_or_404(
            FollowupRecipient.objects.filter(hospital=request.user.hospital), 
            pk=pk
        )
        
        survey = FollowupSurvey.objects.filter(
            recipient=recipient
        ).select_related(
            'template',  # Get the template
            'template__question_1',  # Get all questions through template
            'template__question_2',
            'template__question_3',
            'template__question_4',
            'template__question_5',
            'template__question_6',
            'template__question_7',
            'template__question_8',
            'response'  # Get the response
        ).first()
        
        if not survey:
            return Response(
                {"error": "No survey found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = ManagementSurveyDetailSerializer(survey)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def analyze(self, request):
        """Generate analysis without saving"""
        recipient_ids = request.data.get('recipient_ids', [])
    
        # Filter by hospital at the ViewSet level
        valid_recipient_ids = FollowupRecipient.objects.filter(
            id__in=recipient_ids,
            hospital=request.user.hospital
        ).values_list('id', flat=True)
    
        service = SurveyAnalysisService()
        success, result = service.analyze_surveys(valid_recipient_ids)

        if success:
            return Response(result)
        return Response(
            {'error': result}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @action(detail=False, methods=['post'])
    def save(self, request):
        """Save analysis if user wants to keep it"""
        analysis_result = request.data.get('analysis_result')
        recipient_ids = request.data.get('recipient_ids', [])
        analysis_name = request.data.get('analysis_name')
        
        if not all([analysis_result, recipient_ids, analysis_name]):
            return Response(
                {'error': 'Missing required fields'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        service = SurveyAnalysisService()
        success, result = service.save_analysis(
            analysis_result=analysis_result,
            recipient_ids=recipient_ids,
            analysis_name=analysis_name,
            hospital=request.user.hospital
        )
        
        if success:
            serializer = SurveyAiSerializer(result)
            return Response(serializer.data)
        return Response(
            {'error': result}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )