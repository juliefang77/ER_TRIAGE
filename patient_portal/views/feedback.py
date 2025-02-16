from rest_framework import viewsets, permissions
from rest_framework.response import Response
from patient_portal.models import PatientFeedback
from patient_portal.serializers.feedback_serializer import PatientFeedbackSerializer
from .auth import PatientTokenAuthentication

class PatientFeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = PatientFeedbackSerializer
    authentication_classes = [PatientTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter feedbacks to only show those submitted by the current patient
        """
        return PatientFeedback.objects.filter(patient_user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Automatically set the patient_user when creating feedback
        """
        serializer.save(patient_user=self.request.user)