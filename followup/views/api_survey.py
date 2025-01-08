from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from triage.models import TriageRecord
from rest_framework.viewsets import ViewSet  # Add this import
from ..models import StandardQuestion, SurveyTemplate, FollowupSurvey, FollowupRecipient
from ..serializers.survey_serializer import StandardQuestionSerializer, SurveyTemplateDetailSerializer, MassSendSurveySerializer

# GET question bank questions to make survey template
class StandardQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StandardQuestionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return StandardQuestion.objects.filter(
            is_active=True
        ).order_by('question_category', 'id')

# View existing survey templates, manually create new survey templates
class SurveyTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = SurveyTemplateDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter templates by current user's hospital
        return SurveyTemplate.objects.filter(
            hospital=self.request.user,
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
                hospital=request.user,
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

# GET 我们定义的templates
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
# 群发系统预设surveys给患者app
class MassSendSurveyViewSet(ViewSet):
    """ViewSet for mass sending system survey templates to patients"""
    serializer_class = MassSendSurveySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def assign(self, request):
        """Assign system survey templates to selected patients"""
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        triage_record_ids = serializer.validated_data['triage_record_ids']
        template_id = serializer.validated_data['template_id']

        # Validate it's a system template
        try:
            template = SurveyTemplate.objects.get(
                id=template_id,
                hospital__isnull=True,  # Must be a system template
                is_active=True
            )
        except SurveyTemplate.DoesNotExist:
            return Response(
                {"error": "Invalid system template"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Assign template to selected patients
        surveys_created = []
        for record_id in triage_record_ids:
            # Get the patient and check if they have a PatientUser account
            patient = TriageRecord.objects.get(id=record_id).patient
            if not patient.patient_user:
                continue  # Skip if patient doesn't have an app account
            
            recipient, _ = FollowupRecipient.objects.get_or_create(
                triage_record_id=record_id,
                hospital=request.user,
                defaults={
                    'patient': TriageRecord.objects.get(id=record_id).patient
                }
            )

            survey = FollowupSurvey.objects.create(
                hospital=request.user,
                recipient=recipient,
                template=template,
                status='NO_SEND'
            )
            surveys_created.append(survey)

        return Response({
            "message": f"Successfully assigned system survey to {len(surveys_created)} patients",
            "surveys_created": len(surveys_created)
        })