from rest_framework import viewsets
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

# AI 随访，第一页patient list API
class FollowupRecordDisplayViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FollowupTriageRecordSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_class = FollowupMainFilter
    filter_backends = [
        DjangoFilterBackend
    ]

    ordering = ['-registration_time']  # Default ordering
    ordering_fields = ['registration_time']  # Fields that can be ordered by

    def get_queryset(self):
        # Create subquery for followup check
        followup_exists = FollowupRecipient.objects.filter(
            triage_record=OuterRef('pk'),
            hospital=self.request.user  # Filter by hospital
        )

        # Create subquery for notes check
        notes_exists = FollowupNotetaking.objects.filter(
            patient=OuterRef('patient'),
            hospital=self.request.user  # Filter by hospital
        )

        return TriageRecord.objects.filter(
            hospital=self.request.user
        ).select_related(
            'patient',
            'nurse',
            'hospital',
            'recipient',
            'result'
        ).annotate(
            has_followup=Exists(followup_exists),
            has_note=Exists(notes_exists)  # Add new annotation
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
                hospital=request.user,
                recipient__survey_status='YES_RESPONSE'
            )
            serializer = ManagementSurveyDetailSerializer(survey)
            return Response(serializer.data)
        except FollowupSurvey.DoesNotExist:
            return Response(
                {'error': 'Survey not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
