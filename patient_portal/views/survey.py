from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone

# Import models from followup app
from followup.models import FollowupSurvey, SurveyResponse

# Import serializers (you'll need to create these in patient_portal)
from followup.serializers.survey_serializer import (
    PatientSurveySerializer,
    SurveyResponseSerializer
)
from rest_framework.permissions import AllowAny

class PatientSurveyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PatientSurveySerializer
    permission_classes = [AllowAny]  # Simplified for now

    def get_queryset(self):
        return FollowupSurvey.objects.filter(
            recipient__patient__patient_user=self.request.user,  # More explicit way
            status__in=['NO_SEND', 'NO_RESPONSE']  # Updated status choices
        ).select_related('template')

    @action(detail=True, methods=['post'])
    def submit_response(self, request, pk=None):
        survey = self.get_object()
        
        if survey.status == 'YES_RESPONSE':
            return Response(
                {"error": "Survey already completed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        response_serializer = SurveyResponseSerializer(data=request.data)
        if response_serializer.is_valid():
            SurveyResponse.objects.create(
                hospital=survey.hospital,
                survey=survey,
                submitted_at=timezone.now(),
                **response_serializer.validated_data
            )
            
            survey.status = 'YES_RESPONSE'
            survey.completed_at = timezone.now()
            survey.save()

            return Response({"message": "Survey submitted successfully"})
        
        return Response(
            response_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )