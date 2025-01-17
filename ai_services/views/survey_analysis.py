from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..services.ai_config import SurveyAnalysisPrompts
from ..services.baidu_survey import SurveyAnalysisService
from followup.models import FollowupRecipient, FollowupSurvey
from ..serializers.survey_serializer import SurveyAnalysisListSerializer
from followup.serializers.survey_serializer import ManagementSurveyDetailSerializer

class SurveyAnalysisViewSet(viewsets.ViewSet):
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

        serializer = SurveyAnalysisListSerializer(completed_recipients, many=True)
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
            'template',
            'response'
        ).first()
        
        if not survey:
            return Response(
                {"error": "No survey found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = ManagementSurveyDetailSerializer(survey)
        return Response(serializer.data)
    
    def analyze(self, request):
        recipient_ids = request.data.get('recipient_ids', [])  # Frontend inputs recipient ids
        
        prompt_template = SurveyAnalysisPrompts.get_prompt()
        analysis_service = SurveyAnalysisService(
            recipient_ids=recipient_ids, 
            prompt_template=prompt_template
        )
        
        try:
            result = analysis_service.process()  # What is this??
            return Response(result)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )