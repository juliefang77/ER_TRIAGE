from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from triage.models import TriageRecord
from rest_framework.viewsets import ViewSet  # Add this import
from ..models import StandardQuestion, SurveyTemplate, FollowupSurvey, FollowupRecipient
from ..serializers.survey_serializer import (
    StandardQuestionSerializer, 
    SurveyTemplateDetailSerializer, 
    MassSendSurveySerializer, 
    PatientSurveyHistorySerializer, 
    ManagementSurveyDetailSerializer,
    SurveyTemplateSearchSerializer
)

# GET question bank questions to make survey template
class StandardQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StandardQuestionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return StandardQuestion.objects.filter(
            is_active=True
        ).order_by('question_category', 'id')

# View hospital-created survey templates
class SurveyTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = SurveyTemplateDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter templates by current user's hospital
        return SurveyTemplate.objects.filter(
            hospital=self.request.user.hospital,
            is_active=True
        ).select_related(
            'question_1',
            'question_2',
            'question_3',
            'question_4',
            'question_5',
            'question_6',
            'question_7',
            'question_8'
        ).order_by('-created_at')
    
    @action(detail=False, methods=['post'])
    def create_template(self, request):
        survey_name = request.data.get('survey_name')
        question_ids = request.data.get('question_ids', [])
        creator_name = request.data.get('creator_name', '未知创建者')  # Default value if not provided

        print("Parsed values:", {  # Debug print
        'survey_name': survey_name,
        'question_ids': question_ids,
        'creator_name': creator_name
    })
        
        # Validation
        if not survey_name:
            return Response(
                {"error": "问卷模版名称不能为空"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if not question_ids:
            return Response(
                {"error": "至少需要一个问题"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if len(question_ids) > 8:
            return Response(
                {"error": "最多只能选择8个问题"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create template
            template = SurveyTemplate.objects.create(
                survey_name=survey_name,
                hospital=request.user.hospital,
                created_by=creator_name,  # Just store the name as text
                is_active=True
            )

            # Add questions
            questions = StandardQuestion.objects.filter(id__in=question_ids)
            for index, q_id in enumerate(question_ids, 1):
                question = next((q for q in questions if q.id == q_id), None)
                if question:
                    setattr(template, f'question_{index}', question)
            
            template.save()

            serializer = self.get_serializer(template)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

# GET 我们系统定义的templates (not used)
class SystemTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for system-defined survey templates"""
    serializer_class = SurveyTemplateDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SurveyTemplate.objects.filter(
            hospital__isnull=True,
            is_active=True
        ).select_related(
            'question_1',
            'question_2',
            'question_3',
            'question_4',
            'question_5',
            'question_6',
            'question_7',
            'question_8'
        )

# 群发surveys给患者app
class MassSendSurveyViewSet(ViewSet):
    """ViewSet for mass sending system survey templates to patients"""
    serializer_class = MassSendSurveySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def assign(self, request):
        """Assign survey templates to selected patients"""
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        triage_record_ids = serializer.validated_data['triage_record_ids']
        template_id = serializer.validated_data['template_id']

        # Validate it's a system template
        try:
            template = SurveyTemplate.objects.get(
                id=template_id, # hospital__isnull=True deleted
                is_active=True
            )
        except SurveyTemplate.DoesNotExist:
            return Response(
                {"error": "Invalid system template"},
                status=status.HTTP_400_BAD_REQUEST
            )

        surveys_created = []
        skipped_patients = []  # Track skipped patients for reporting

        for record_id in triage_record_ids:
            # Get the patient record
            patient = TriageRecord.objects.get(id=record_id).patient
            
            # Get the PatientUser
            patient_user = patient.patient_user
            if not patient_user:
                continue  # Skip if patient doesn't have an app account

            # Check if patient already has a survey (NOT_SENT is okay)
            existing_recipient = FollowupRecipient.objects.filter(
                triage_record_id=record_id,
                hospital=request.user.hospital,
                survey_status__in=['NO_RESPONSE', 'YES_RESPONSE']
            ).exists()

            if existing_recipient:
                skipped_patients.append(record_id)
                continue  # Skip this patient

            # Update get_or_create to include patient_user
            recipient, _ = FollowupRecipient.objects.get_or_create(
                triage_record_id=record_id,
                hospital=request.user.hospital,
                defaults={
                    'patient': patient,
                    'patient_user': patient_user,  # Add this line
                    'message_reply': 'NOT_SENT',
                    'survey_status': 'NO_RESPONSE',  
                    'call_status': 'NO_CALL'
                }
            )

            survey = FollowupSurvey.objects.create(
                hospital=request.user.hospital,
                recipient=recipient,
                template=template
            )
            surveys_created.append(survey)

        return Response({
            "message": f"Successfully assigned system survey to {len(surveys_created)} patients. Skipped {len(skipped_patients)} patients who already have surveys.",
            "surveys_created": len(surveys_created),
            "skipped_patients": len(skipped_patients)
        })

# 查看过去发送的 surveys list (not used)
class ManagementSurveyHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ManagementSurveyDetailSerializer
        return PatientSurveyHistorySerializer

    def get_queryset(self):
        queryset = FollowupSurvey.objects.filter(
            hospital=self.request.user.hospital
        )
        
        if self.action == 'retrieve':
            # Add more related fields for detailed view
            queryset = queryset.select_related(
                'recipient__patient',
                'template',
                'response'  # If you have a response model
            ).prefetch_related(
                'template__question_1',
                'template__question_2',
                'template__question_3',
                'template__question_4',
                'template__question_5',
                'template__question_6',
                'template__question_7',
                'template__question_8'
            )
        else:
            # Basic related fields for list view
            queryset = queryset.select_related(
                'recipient__patient',
                'template'
            )
        
        return queryset.order_by('-created_at')

# 人工发送问卷页面，左上角“选择问卷模版” search function
class SurveyTemplateSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for searching available templates when sending surveys"""
    serializer_class = SurveyTemplateSearchSerializer  # Use simpler serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        search_query = self.request.query_params.get('search', '')
        return SurveyTemplate.objects.filter(
            hospital=self.request.user.hospital,
            is_active=True,
            survey_name__icontains=search_query
        ).order_by('-created_at')  # No need for select_related since we don't use questions