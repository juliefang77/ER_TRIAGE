from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from triage.models import TriageRecord
from ..models import FollowupRecipient, FollowupNotetaking, FollowupSurvey
from ..serializers.recorddisplay_serializer import FollowupTriageRecordSerializer
from ..serializers.survey_serializer import ManagementSurveyDetailSerializer
from django.db.models import Exists, OuterRef
from followup.filters import FollowupMainFilter
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter  # Import OrderingFilter directly
from rest_framework.pagination import PageNumberPagination

# Add pagination class (at the top of your file)
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# AI 随访，第一页patient list API
class FollowupRecordDisplayViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FollowupTriageRecordSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_class = FollowupMainFilter
    filter_backends = [
        DjangoFilterBackend
    ]
    pagination_class = StandardResultsSetPagination  # Add this line

    ordering = ['-registration_time']  # Default ordering
    ordering_fields = ['registration_time']  # Fields that can be ordered by

    def get_queryset(self):
        # Create subquery for followup check
        followup_exists = FollowupRecipient.objects.filter(
            triage_record=OuterRef('pk'),
            hospital=self.request.user.hospital  # Filter by hospital
        )

        # Create subquery for notes check
        notes_exists = FollowupNotetaking.objects.filter(
            patient=OuterRef('patient'),
            hospital=self.request.user.hospital  # Filter by hospital
        )

        return TriageRecord.objects.filter(
            hospital=self.request.user.hospital
        ).select_related(
            'patient',
            'hospital',
            'recipient',
            'result',
            'vitalsigns'
        ).annotate(
            has_followup=Exists(followup_exists),
            has_note=Exists(notes_exists)  # Add new annotation
        )
    
    # Mark research_patient 小红旗
    @action(detail=True, methods=['post'])
    def toggle_research_status(self, request, pk=None):
        """Toggle research_patient status for a recipient"""
        try:
            # Get the recipient for this triage record
            recipient = FollowupRecipient.objects.get(
                triage_record_id=pk,
                hospital=request.user.hospital
            )
            
            # Toggle the status
            recipient.research_patient = not recipient.research_patient
            recipient.save()
            
            return Response({
                'message': 'Research status updated successfully',
                'research_patient': recipient.research_patient,
                'triage_record_id': pk
            })
            
        except FollowupRecipient.DoesNotExist:
            # If recipient doesn't exist, create one with research_patient=True
            try:
                triage_record = TriageRecord.objects.get(
                    id=pk,
                    hospital=request.user.hospital
                )
                recipient = FollowupRecipient.objects.create(
                    triage_record=triage_record,
                    hospital=request.user.hospital,
                    patient=triage_record.patient,
                    patient_user=triage_record.patient.patient_user,
                    research_patient=True
                )
                return Response({
                    'message': 'Recipient created with research status enabled',
                    'research_patient': True,
                    'triage_record_id': pk
                })
                
            except TriageRecord.DoesNotExist:
                return Response(
                    {'error': 'Triage record not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

# 小眼睛看survey results
class SurveyEyeViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        # pk will be the triage_record_id
        try:
            survey = FollowupSurvey.objects.select_related(
                'recipient',
                'template',
                'response'
            ).get(
                recipient__triage_record_id=pk,
                hospital=request.user.hospital,
                recipient__survey_status='YES_RESPONSE'
            )
            serializer = ManagementSurveyDetailSerializer(survey)
            return Response(serializer.data)
        except FollowupSurvey.DoesNotExist:
            return Response(
                {'error': 'Survey not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
