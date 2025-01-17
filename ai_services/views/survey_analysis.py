from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..services.baidu_survey import SurveyAnalysisService
from followup.models import FollowupRecipient, FollowupSurvey
# Serializers
from ..serializers.survey_serializer import SurveyAnalysisListSerializer, SurveyAiSerializer
from followup.serializers.survey_serializer import ManagementSurveyDetailSerializer
# Filters
from followup.filters import AiSurveyRecipientFilter
from django_filters.rest_framework import DjangoFilterBackend

class SurveyAnalysisViewSet(viewsets.ViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = AiSurveyRecipientFilter

    def list(self, request):
        # Get completed surveys with related data
        completed_recipients = FollowupRecipient.objects.filter(
            survey_status='YES_RESPONSE',
            hospital=request.user
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

        serializer = SurveyAnalysisListSerializer(filtered_recipients, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def survey_detail(self, request, pk=None):
        # Get the specific recipient's survey details
        recipient = get_object_or_404(
            FollowupRecipient.objects.filter(hospital=request.user), 
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
            hospital=request.user
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
            hospital=request.user
        )
        
        if success:
            serializer = SurveyAiSerializer(result)
            return Response(serializer.data)
        return Response(
            {'error': result}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )